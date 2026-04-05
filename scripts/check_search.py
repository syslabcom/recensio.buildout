"""Compare Plone catalog and Solr indexes.

Usage:
    bin/instance run scripts/check_search.py <portal_id>
    bin/zopepy scripts/check_search.py  (requires manual site setup)
"""

import csv
import os
import sys
from collections import Counter

from AccessControl.SecurityManagement import newSecurityManager
from collective.solr.interfaces import ISolrConnectionManager
from collective.solr.parser import SolrResponse
from Testing.makerequest import makerequest
from zope.component import queryUtility
from zope.component.hooks import setSite

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir, "var", "tmp"
)
CATALOG_FILE = os.path.join(OUTPUT_DIR, "catalog_items.csv")
SOLR_FILE = os.path.join(OUTPUT_DIR, "solr_items.csv")
DIFF_FILE = os.path.join(OUTPUT_DIR, "diff_items.csv")


def dump_csv(filepath, rows):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "path", "title", "portal_type", "UID"])
        for row in sorted(rows, key=lambda r: r["path"]):
            writer.writerow(
                [row["id"], row["path"], row["title"], row["portal_type"], row["UID"]]
            )


def check_catalog(portal):
    catalog = portal.portal_catalog
    brains = catalog.searchResults()
    total = len(brains)
    type_counts = Counter()
    rows = []
    for brain in brains:
        portal_type = brain.portal_type or ""
        type_counts[portal_type] += 1
        title = brain.Title
        if callable(title):
            title = title()
        rows.append(
            {
                "id": brain.getId or "",
                "path": brain.getPath() or "",
                "title": title or "",
                "portal_type": portal_type,
                "UID": brain.UID or "",
            }
        )
    print("\n=== Plone Catalog ===")
    print(f"Total indexed items: {total}")
    print("\nPer portal_type:")
    for ptype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {ptype or '(empty)'}: {count}")
    dump_csv(CATALOG_FILE, rows)
    print(f"\nDumped to {os.path.abspath(CATALOG_FILE)}")
    return {r["UID"]: r for r in rows if r["UID"]}


def check_solr(portal):
    manager = queryUtility(ISolrConnectionManager)
    if manager is None:
        print("\n=== Solr ===")
        print("ERROR: No Solr connection manager found. Is collective.solr active?")
        return set()
    conn = manager.getConnection()
    if conn is None:
        print("\n=== Solr ===")
        print("ERROR: Could not get Solr connection.")
        return set()

    # First query to get total count
    response = conn.search(q="*:*", rows=0, fl="UID")
    result = SolrResponse(response.read())
    total = int(result.response.numFound)

    # Fetch all documents in batches
    rows = []
    batch_size = 5000
    for start in range(0, total, batch_size):
        response = conn.search(
            q="*:*",
            rows=batch_size,
            start=start,
            fl="UID,Title,path_string,portal_type,id",
            sort="UID asc",
        )
        result = SolrResponse(response.read())
        for doc in result.response:
            rows.append(
                {
                    "id": getattr(doc, "id", "") or "",
                    "path": getattr(doc, "path_string", "") or "",
                    "title": getattr(doc, "Title", "") or "",
                    "portal_type": getattr(doc, "portal_type", "") or "",
                    "UID": getattr(doc, "UID", "") or "",
                }
            )

    type_counts = Counter(r["portal_type"] for r in rows)
    print(f"\n=== Solr ===")
    print(f"Total indexed items: {total}")
    print("\nPer portal_type:")
    for ptype, count in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {ptype or '(empty)'}: {count}")
    dump_csv(SOLR_FILE, rows)
    print(f"\nDumped to {os.path.abspath(SOLR_FILE)}")
    return {r["UID"]: r for r in rows if r["UID"]}


def format_row(row):
    return (
        f"  UID={row['UID']}  type={row['portal_type']}"
        f"  id={row['id']}  path={row['path']}"
        f"  title={row['title']}"
    )


def compare(catalog_items, solr_items):
    catalog_uids = set(catalog_items)
    solr_uids = set(solr_items)
    only_catalog = catalog_uids - solr_uids
    only_solr = solr_uids - catalog_uids
    common = catalog_uids & solr_uids
    print("\n=== Comparison (by UID) ===")
    print(f"In both:         {len(common)}")
    print(f"Only in catalog: {len(only_catalog)}")
    print(f"Only in Solr:    {len(only_solr)}")
    if only_catalog:
        print(f"\nItems only in catalog ({len(only_catalog)}):")
        for uid in sorted(only_catalog):
            print(format_row(catalog_items[uid]))
    if only_solr:
        print(f"\nItems only in Solr ({len(only_solr)}):")
        for uid in sorted(only_solr):
            print(format_row(solr_items[uid]))

    # Dump diff to CSV
    os.makedirs(os.path.dirname(DIFF_FILE), exist_ok=True)
    with open(DIFF_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "id", "path", "title", "portal_type", "UID"])
        for uid in sorted(only_catalog):
            r = catalog_items[uid]
            writer.writerow(["catalog", r["id"], r["path"], r["title"], r["portal_type"], r["UID"]])
        for uid in sorted(only_solr):
            r = solr_items[uid]
            writer.writerow(["solr", r["id"], r["path"], r["title"], r["portal_type"], r["UID"]])
    print(f"\nDiff dumped to {os.path.abspath(DIFF_FILE)}")


def main(app):
    portal_id = sys.argv[-1] if len(sys.argv) > 3 else None
    app = makerequest(app)

    if portal_id and portal_id in app.objectIds():
        portal = app[portal_id]
    else:
        sites = app.objectValues("Plone Site")
        if not sites:
            print("No Plone site found.")
            sys.exit(1)
        portal = sites[0]
        print(f"Using site: {portal.getId()}")

    setSite(portal)

    # Impersonate admin so catalog queries are unrestricted
    admin = app.acl_users.getUserById("admin")
    if admin is None:
        # Try the root user folder
        admin = app.acl_users.getUser("admin")
    if admin is not None:
        newSecurityManager(None, admin.__of__(app.acl_users))
    else:
        print("WARNING: Could not find admin user, catalog may return no results.")

    catalog_items = check_catalog(portal)
    solr_items = check_solr(portal)
    compare(catalog_items, solr_items)


main(app)  # noqa: F821
