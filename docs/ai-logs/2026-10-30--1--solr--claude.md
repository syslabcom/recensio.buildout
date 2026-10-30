## thet

I'm having troubles getting solr to work on our staging server.

The solr logs after solr startup show:

```

*** [WARN] *** Your open file limit is currently 1024.
 It should be set to 65000 to avoid operational disruption.
 If you no longer wish to see this warning, set SOLR_ULIMIT_CHECKS to false in your profile or solr.in.sh
*** [WARN] ***  Your Max Processes Limit is currently 31442.
 It should be set to 65000 to avoid operational disruption.
 If you no longer wish to see this warning, set SOLR_ULIMIT_CHECKS to false in your profile or solr.in.sh
Java 21 detected. Enabled workaround for SOLR-16463
Java 21 detected. Incubating Panama Vector APIs have been enabled
[0.007s][warning][pagesize] UseLargePages disabled, no large pages configured and available on the system.
CompileCommand: exclude com/github/benmanes/caffeine/cache/BoundedLocalCache.put bool exclude = true
2026-10-30 08:28:13.705 INFO  (main) [c: s: r: x: t:] o.e.j.s.Server jetty-10.0.22; built: 2024-06-27T16:03:51.502Z; git: 5c8471e852d377fd726ad9b1692c35ffc5febb09; jvm 21.0.12.1+1-1-24.04.4-Ubuntu
2026-10-30 08:28:14.274 WARN  (main) [c: s: r: x: t:] o.e.j.u.DeprecationWarning Using @Deprecated Class org.eclipse.jetty.servlet.listener.ELContextCleaner
2026-10-30 08:28:14.316 INFO  (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider Using logger factory org.apache.logging.slf4j.Log4jLoggerFactory
2026-10-30 08:28:14.328 INFO  (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider  ___      _       Welcome to Apache Solr™ version 9.10.1
2026-10-30 08:28:14.329 INFO  (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider / __| ___| |_ _   Starting in standalone mode on port 8983
2026-10-30 08:28:14.330 INFO  (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider \__ \/ _ \ | '_|  Install dir: /home/plone/recensio/solr
2026-10-30 08:28:14.330 INFO  (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider |___/\___/_|_|    Start time: 2026-10-30T08:28:14.330097570Z
2026-10-30 08:28:14.333 INFO  (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider Solr started with "-XX:+CrashOnOutOfMemoryError" that will crash on any OutOfMemoryError exception. The cause of the OOME will be logged in the crash file at the following path: /home/plone/recensio/solr/server/logs/jvm_crash_2701218.log
2026-10-30 08:28:14.484 INFO  (main) [c: s: r: x: t:] o.a.l.s.MemorySegmentIndexInputProvider Using MemorySegmentIndexInput and native madvise support with Java 21 or later; to disable start with -Dorg.apache.lucene.store.MMapDirectory.enableMemorySegments=false
2026-10-30 08:28:14.537 INFO  (main) [c: s: r: x: t:] o.a.l.i.v.PanamaVectorizationProvider Java vector incubator API enabled; uses preferredBitSize=256; FMA enabled
2026-10-30 08:28:14.544 INFO  (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider Solr Home: /home/plone/recensio/solr/server/solr (source: system property: solr.solr.home)
2026-10-30 08:28:14.573 INFO  (main) [c: s: r: x: t:] o.a.s.c.SolrResourceLoader Added 96 libs to classloader, from paths: [/home/plone/recensio/solr/modules/extraction/lib]
2026-10-30 08:28:14.574 INFO  (main) [c: s: r: x: t:] o.a.s.c.NodeConfig Added module extraction. libPath=/home/plone/recensio/solr/modules/extraction/lib with 96 libs
2026-10-30 08:28:14.912 INFO  (main) [c: s: r: x: t:] o.a.s.c.SolrXmlConfig Loading solr.xml from /home/plone/recensio/solr/server/solr/solr.xml
2026-10-30 08:28:14.962 ERROR (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider Could not start Solr. Check solr/home property and the logs => org.apache.solr.common.SolrException: Unknown configuration value in solr.xml: allowZkHosts
 at org.apache.solr.core.SolrXmlConfig.lambda$fillSolrSection$2(SolrXmlConfig.java:414)
org.apache.solr.common.SolrException: Unknown configuration value in solr.xml: allowZkHosts
 at org.apache.solr.core.SolrXmlConfig.lambda$fillSolrSection$2(SolrXmlConfig.java:414) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.lambda$forEachNamedListEntry$3(SolrXmlConfig.java:655) ~[?:?]
 at java.base/java.lang.Iterable.forEach(Iterable.java:75) ~[?:?]
 at org.apache.solr.util.DataConfigNode.lambda$forEachChild$5(DataConfigNode.java:141) ~[?:?]
 at java.base/java.util.Map.forEach(Map.java:733) ~[?:?]
 at org.apache.solr.util.DataConfigNode.forEachChild(DataConfigNode.java:138) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.forEachNamedListEntry(SolrXmlConfig.java:652) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.fillSolrSection(SolrXmlConfig.java:332) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.fromConfig(SolrXmlConfig.java:190) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.fromInputStream(SolrXmlConfig.java:244) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.fromInputStream(SolrXmlConfig.java:230) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.fromFile(SolrXmlConfig.java:213) ~[?:?]
 at org.apache.solr.core.SolrXmlConfig.fromSolrHome(SolrXmlConfig.java:259) ~[?:?]
 at org.apache.solr.core.NodeConfig.loadNodeConfig(NodeConfig.java:285) ~[?:?]
 at org.apache.solr.servlet.CoreContainerProvider.createCoreContainer(CoreContainerProvider.java:406) ~[?:?]
 at org.apache.solr.servlet.CoreContainerProvider.init(CoreContainerProvider.java:231) ~[?:?]
 at org.apache.solr.servlet.CoreContainerProvider.contextInitialized(CoreContainerProvider.java:108) ~[?:?]
 at org.eclipse.jetty.server.handler.ContextHandler.callContextInitialized(ContextHandler.java:1049) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletContextHandler.callContextInitialized(ServletContextHandler.java:624) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ContextHandler.contextInitialized(ContextHandler.java:984) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:740) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:392) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1304) ~[jetty-webapp-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:901) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletContextHandler.doStart(ServletContextHandler.java:306) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:532) ~[jetty-webapp-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:121) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:121) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.gzip.GzipHandler.doStart(GzipHandler.java:221) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.Server.start(Server.java:470) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.Server.doStart(Server.java:415) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.xml.XmlConfiguration.main(XmlConfiguration.java:1919) ~[jetty-xml-10.0.22.jar:10.0.22]
 at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103) ~[?:?]
 at java.base/java.lang.reflect.Method.invoke(Method.java:580) ~[?:?]
 at org.eclipse.jetty.start.Main.invokeMain(Main.java:229) ~[start.jar:10.0.26]
 at org.eclipse.jetty.start.Main.start(Main.java:528) ~[start.jar:10.0.26]
 at org.eclipse.jetty.start.Main.main(Main.java:76) ~[start.jar:10.0.26]
2026-10-30 08:28:14.985 ERROR (main) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider Error processing the request. CoreContainer has shut down.
2026-10-30 08:28:14.986 ERROR (main) [c: s: r: x: t:] o.a.s.s.SolrDispatchFilter Could not start Dispatch Filter. => javax.servlet.UnavailableException: Error processing the request. CoreContainer has shut down.
 at org.apache.solr.servlet.CoreContainerProvider.checkReady(CoreContainerProvider.java:141)
javax.servlet.UnavailableException: Error processing the request. CoreContainer has shut down.
 at org.apache.solr.servlet.CoreContainerProvider.checkReady(CoreContainerProvider.java:141) ~[?:?]
 at org.apache.solr.servlet.CoreContainerProvider.getCoreContainer(CoreContainerProvider.java:122) ~[?:?]
 at org.apache.solr.servlet.SolrDispatchFilter.getCores(SolrDispatchFilter.java:162) ~[?:?]
 at org.apache.solr.servlet.SolrDispatchFilter.init(SolrDispatchFilter.java:140) ~[?:?]
 at org.eclipse.jetty.servlet.FilterHolder.initialize(FilterHolder.java:133) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletHandler.lambda$initialize$2(ServletHandler.java:725) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at java.base/java.util.ArrayList$ArrayListSpliterator.forEachRemaining(ArrayList.java:1708) ~[?:?]
 at java.base/java.util.stream.Streams$ConcatSpliterator.forEachRemaining(Streams.java:734) ~[?:?]
 at java.base/java.util.stream.ReferencePipeline$Head.forEach(ReferencePipeline.java:762) ~[?:?]
 at org.eclipse.jetty.servlet.ServletHandler.initialize(ServletHandler.java:749) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletContextHandler.startContext(ServletContextHandler.java:392) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.webapp.WebAppContext.startContext(WebAppContext.java:1304) ~[jetty-webapp-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ContextHandler.doStart(ContextHandler.java:901) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletContextHandler.doStart(ServletContextHandler.java:306) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.webapp.WebAppContext.doStart(WebAppContext.java:532) ~[jetty-webapp-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:121) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:121) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.gzip.GzipHandler.doStart(GzipHandler.java:221) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.start(ContainerLifeCycle.java:171) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.Server.start(Server.java:470) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.ContainerLifeCycle.doStart(ContainerLifeCycle.java:114) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.AbstractHandler.doStart(AbstractHandler.java:89) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.Server.doStart(Server.java:415) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.component.AbstractLifeCycle.start(AbstractLifeCycle.java:93) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.xml.XmlConfiguration.main(XmlConfiguration.java:1919) ~[jetty-xml-10.0.22.jar:10.0.22]
 at java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103) ~[?:?]
 at java.base/java.lang.reflect.Method.invoke(Method.java:580) ~[?:?]
 at org.eclipse.jetty.start.Main.invokeMain(Main.java:229) ~[start.jar:10.0.26]
 at org.eclipse.jetty.start.Main.start(Main.java:528) ~[start.jar:10.0.26]
 at org.eclipse.jetty.start.Main.main(Main.java:76) ~[start.jar:10.0.26]
2026-10-30 08:28:15.007 INFO  (main) [c: s: r: x: t:] o.e.j.s.h.ContextHandler Started o.e.j.w.WebAppContext@125c082e{solr-jetty-context.xml,/solr,file:///home/plone/recensio/solr/server/solr-webapp/webapp/,AVAILABLE}{/home/plone/recensio/solr/server/solr-webapp/webapp}
2026-10-30 08:28:15.023 INFO  (main) [c: s: r: x: t:] o.e.j.s.RequestLogWriter Opened /home/plone/recensio/solr/server/logs/2026_10_30.request.log
2026-10-30 08:28:15.033 INFO  (main) [c: s: r: x: t:] o.e.j.s.AbstractConnector Started ServerConnector@142eef62{HTTP/1.1, (http/1.1, h2c)}{127.0.0.1:8983}
2026-10-30 08:28:15.035 INFO  (main) [c: s: r: x: t:] o.e.j.s.Server Started Server@2af616d3{STARTING}[10.0.22,sto=0] @3407ms
```

When searching in Plone I get this error in Plone:

```
2026-10-30 09:30:01,642 ERROR   [Zope.SiteErrorLog:35][waitress-2] SolrConnectionException: http://localhost:9090/recensio/themen-epochen-regionen/@@browse-topics
Traceback (innermost last):
  Module ZPublisher.WSGIPublisher, line 179, in transaction_pubevents
  Module ZPublisher.WSGIPublisher, line 388, in publish_module
  Module ZPublisher.WSGIPublisher, line 282, in publish
  Module ZPublisher.mapply, line 98, in mapply
  Module ZPublisher.WSGIPublisher, line 68, in call_object
  Module recensio.plone.browser.topical, line 67, in __call__
  Module Products.Five.browser.pagetemplatefile, line 127, in __call__
  Module Products.Five.browser.pagetemplatefile, line 59, in __call__
  Module zope.pagetemplate.pagetemplate, line 134, in pt_render
  Module Products.PageTemplates.engine, line 368, in __call__
  Module z3c.pt.pagetemplate, line 207, in render
  Module chameleon.zpt.template, line 359, in render
  Module chameleon.template, line 268, in render
  Module chameleon.utils, line 52, in raise_with_traceback
  Module chameleon.template, line 238, in render
  Module 82d57664db10dc552df86ec5427dd929, line 4258, in render
  Module f21db20f95a1f4d46eea1ec3c91a8d9e, line 926, in render_master
  Module f21db20f95a1f4d46eea1ec3c91a8d9e, line 1473, in render_content
  Module 82d57664db10dc552df86ec5427dd929, line 1507, in __fill_main
  Module zope.tales.expressions, line 248, in __call__
  Module Products.PageTemplates.Expressions, line 217, in _eval
  Module zope.tales.expressions, line 153, in _eval
  Module Products.PageTemplates.Expressions, line 133, in trustedBoboAwareZopeTraverse
  Module zope.traversing.adapters, line 149, in traversePathElement
   - __traceback_info__: (<Products.Five.browser.metaconfigure.SimpleViewClass from /home/plone/recensio/.venv/lib/python3.11/site-packages/recensio/plone/browser/templates/topical.pt object at 0x77b6ecec4710>, 'results')
  Module zope.traversing.adapters, line 46, in traverse
   - __traceback_info__: (<Products.Five.browser.metaconfigure.SimpleViewClass from /home/plone/recensio/.venv/lib/python3.11/site-packages/recensio/plone/browser/templates/topical.pt object at 0x77b6ecec4710>, 'results', [])
  Module plone.memoize.view, line 51, in memogetter
  Module recensio.plone.browser.topical, line 186, in results
  Module collective.solr.monkey, line 19, in searchResults
  Module collective.solr.dispatcher, line 36, in __call__
  Module collective.solr.dispatcher, line 87, in solrSearchResults
  Module collective.solr.search, line 155, in buildQueryAndParameters
  Module collective.solr.manager, line 170, in getSchema
  Module collective.solr.solr, line 265, in get_schema
  Module collective.solr.solr, line 426, in getSchema
  Module collective.solr.solr, line 156, in __errcheck
collective.solr.exceptions.SolrConnectionException: collective.solr.exceptions.SolrConnectionException: HTTP code=404, reason=Not Found

 - Expression: "context/main_template/macros/master"
 - Filename:   ... ite-packages/recensio/plone/browser/templates/topical.pt
 - Location:   (line 6: col 23)
 - Source:     ... etal:use-macro="context/main_template/macros/master"
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 - Arguments:  template: <Products.Five.browser.pagetemplatefile.ViewPageTemplateFile object at 0x77b6e50def10>
               options: {}
               args: ()
               nothing: None
               modules: <Products.PageTemplates.ZRPythonExpr._SecureModuleImporter object at 0x77b6f0bf8210>
               request: <WSGIRequest, URL=http://localhost:9090/recensio/themen-epochen-regionen/@@browse-topics>
               view: <Products.Five.browser.metaconfigure.SimpleViewClass from /home/plone/recensio/.venv/lib/python3.11/site-packages/recensio/plone/browser/templates/topical.pt object at 0x77b6ecec4710>
               context: <Folder at /recensio/themen-epochen-regionen>
               views: <Products.Five.browser.pagetemplatefile.ViewMapper object at 0x77b6ed04a2d0>
               here: <Folder at /recensio/themen-epochen-regionen>
               container: <Folder at /recensio/themen-epochen-regionen>
               root: <Application at >
               traverse_subpath: []
               user: <PropertiedUser 'admin'>
               default: <DEFAULT>
               repeat: <Products.PageTemplates.engine.RepeatDictWrapper object at 0x77b6e7f04d20>
               loop: {}
               target_language: None
               translate: <function BaseTemplate.render.<locals>.translate at 0x77b6e3d7d260>
               macroname: 'master'
               attrs: {}
```

And the solr logs show:

```

2026-10-30 08:30:01.538 ERROR (qtp1632670136-26) [c: s: r: x: t:] o.a.s.s.CoreContainerProvider Error processing the request. CoreContainer has shut down.
2026-10-30 08:30:01.540 WARN  (qtp1632670136-26) [c: s: r: x: t:] o.e.j.s.HttpChannel /solr/plone/admin/file/ => javax.servlet.ServletException: javax.servlet.UnavailableException: Error processing the request. CoreContainer has shut down.
 at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:157)
javax.servlet.ServletException: javax.servlet.UnavailableException: Error processing the request. CoreContainer has shut down.
 at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:157) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:122) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.rewrite.handler.RewriteHandler.handle(RewriteHandler.java:301) ~[jetty-rewrite-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:122) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.gzip.GzipHandler.handle(GzipHandler.java:822) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:122) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.Server.handle(Server.java:563) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.HttpChannel$RequestDispatchable.dispatch(HttpChannel.java:1598) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.HttpChannel.dispatch(HttpChannel.java:753) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.HttpChannel.handle(HttpChannel.java:501) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.HttpConnection.onFillable(HttpConnection.java:287) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.io.AbstractConnection$ReadCallback.succeeded(AbstractConnection.java:314) ~[jetty-io-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.io.FillInterest.fillable(FillInterest.java:100) ~[jetty-io-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.io.SelectableChannelEndPoint$1.run(SelectableChannelEndPoint.java:53) ~[jetty-io-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.thread.QueuedThreadPool.runJob(QueuedThreadPool.java:969) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.thread.QueuedThreadPool$Runner.doRunJob(QueuedThreadPool.java:1194) ~[jetty-util-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.util.thread.QueuedThreadPool$Runner.run(QueuedThreadPool.java:1149) ~[jetty-util-10.0.22.jar:10.0.22]
 at java.base/java.lang.Thread.run(Thread.java:1583) [?:?]
Caused by: javax.servlet.UnavailableException: Error processing the request. CoreContainer has shut down.
 at org.apache.solr.servlet.CoreContainerProvider.checkReady(CoreContainerProvider.java:141) ~[?:?]
 at org.apache.solr.servlet.CoreContainerProvider.getCoreContainer(CoreContainerProvider.java:122) ~[?:?]
 at org.apache.solr.servlet.SolrDispatchFilter.getCores(SolrDispatchFilter.java:162) ~[?:?]
 at org.apache.solr.servlet.SolrDispatchFilter.doFilter(SolrDispatchFilter.java:178) ~[?:?]
 at javax.servlet.http.HttpFilter.doFilter(HttpFilter.java:97) ~[jetty-servlet-api-4.0.6.jar:?]
 at org.eclipse.jetty.servlet.FilterHolder.doFilter(FilterHolder.java:210) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletHandler$Chain.doFilter(ServletHandler.java:1635) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletHandler.doHandle(ServletHandler.java:527) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:131) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.security.SecurityHandler.handle(SecurityHandler.java:598) ~[jetty-security-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.HandlerWrapper.handle(HandlerWrapper.java:122) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ScopedHandler.nextHandle(ScopedHandler.java:223) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.session.SessionHandler.doHandle(SessionHandler.java:1580) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ScopedHandler.nextHandle(ScopedHandler.java:221) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ContextHandler.doHandle(ContextHandler.java:1384) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ScopedHandler.nextScope(ScopedHandler.java:176) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.servlet.ServletHandler.doScope(ServletHandler.java:484) ~[jetty-servlet-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.session.SessionHandler.doScope(SessionHandler.java:1553) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ScopedHandler.nextScope(ScopedHandler.java:174) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ContextHandler.doScope(ContextHandler.java:1306) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ScopedHandler.handle(ScopedHandler.java:129) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.ContextHandlerCollection.handle(ContextHandlerCollection.java:149) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.InetAccessHandler.handle(InetAccessHandler.java:228) ~[jetty-server-10.0.22.jar:10.0.22]
 at org.eclipse.jetty.server.handler.HandlerCollection.handle(HandlerCollection.java:141) ~[jetty-server-10.0.22.jar:10.0.22]
 ... 17 more
```

What is it?

Note: We recently had to upgrade solr from 9.10.1 to 9.11.0.

## CodeCompanion (Codex)

I’ll check the repository’s Solr setup and the version-specific configuration. The first fatal error is `Unknown configuration value in solr.xml: allowZkHosts`; the later Plone error follows Solr’s failed startup.

**Execute** pwd; rg --files -g AGENTS.md -g '\*solr\*' -g '\*Solr\*' -g '...

**Search** Web search

**Execute** rg -n 'solr|tar |extract' Makefile config/solr.cfg; rg -n...

This is a **mixed-version Solr installation after the upgrade**.

Your startup log still says:

```text
Welcome to Apache Solr™ version 9.10.1
```

But `solr.xml` contains `allowZkHosts`, which was **introduced in 9.11.0**. The older code rejects that configuration and shuts down the CoreContainer. [Apache release notes](https://cwiki.apache.org/confluence/spaces/SOLR/pages/421958427/ReleaseNote9_11_0)

I found the likely cause in [Makefile](/home/_thet/data/dev/syslab/REPOS/recensio/recensio.buildout-plone6/Makefile:49): it extracts the new archive **over the existing `solr/` directory**. This leaves old, version-named JARs alongside the new ones. Your local installation actually contains `solr-core-9.9.0.jar`, `solr-core-9.10.1.jar`, and `solr-core-9.11.0.jar` together.

To fix staging:

1. Stop Solr using its supervisor/service manager.
2. Preserve the existing installation, especially core data and custom configuration.
3. Extract 9.11.0 into a **fresh directory**.
4. Restore the `plone` core configuration and data, preserving any symlinks.
5. Start Solr and verify the log reports **9.11.0**, with no CoreContainer initialization errors.

Check staging for the same leftover JARs:

```bash
ls /home/plone/recensio/solr/server/solr-webapp/webapp/WEB-INF/lib/solr-core-*.jar
```

After repair, verify the core:

```bash
curl -fsS 'http://127.0.0.1:8983/solr/admin/cores?action=STATUS&core=plone&wt=json'
```

The Plone schema-fetch error is downstream of the failed startup. Jetty still listens on port 8983, but Solr itself is unavailable. The file/process-limit and large-page warnings did **not** cause this failure.

Removing `allowZkHosts` alone would leave the mixed JAR installation unresolved. The Makefile’s upgrade procedure also needs to use a clean installation directory.

## thet

Great! Please fix the Makefile for me, so that this process is automated and future updates don't have the same problem.

## CodeCompanion (Codex)

I’ll update the Makefile to install each Solr release cleanly while preserving core data and configuration, then check the upgrade behavior.

**Execute** cat Makefile; cat .gitignore; ls -ld etc/solr solr/server...

**Execute** rg -n 'solr|supervisor' config/supervisor\* config/solr.cf...

**Execute** rg -n 'solr|programs' config/base.cfg profiles/\*.cfg \*.cf...

### Reasoning

**Planning Makefile staging**

**Preparing Makefile staging**

### Response

The Makefile currently extracts directly into the live installation. I’ll change it to prepare a fresh installation, preserve the Solr home’s core data and configuration, and keep the previous directory as a backup. A version marker will trigger this migration for the existing mixed installation too. Solr will need to be stopped before running the upgrade.

**Edit** .gitignore

### Reasoning

**Testing archive timestamps**

### Response

**Execute** python3 - <<'PY' import pathlib, tempfile, shutil, tarfil...

### Reasoning

**Fixing default configset copies**

### Response

Updated [Makefile](/home/_thet/data/dev/syslab/REPOS/recensio/recensio.buildout-plone6/Makefile:45) to:

- Extract each release into a fresh directory.
- Preserve core data, configuration, and symlinks.
- Keep the previous installation in `solr.backup.*`.
- Detect upgrades using a version marker.
- Reject failed downloads before installation.

Verified fresh installs, upgrades, stale JAR removal, data preservation, repeat runs, and failed extraction handling using temporary fixtures.

On staging, run:

```bash
bin/supervisorctl stop solr
make solr
bin/supervisorctl start solr
```

Future upgrades require updating `SOLR_VERSION` and `config/solr.cfg`. Backups include index data, so allow sufficient disk space.

## thet

Why the names `.solr-install.XXXXXX` and `solr.backup.XXXXXX`? wouldn't it be better to use the current date+time instead of `XXXXXX`?

## CodeCompanion (Codex)

`XXXXXX` is a placeholder for `mktemp`: it generates a unique suffix, such as `solr.backup.a8Kp2z`. This avoids collisions and creates the directory atomically.

A timestamp would make backups easier to identify. A good combination is:

```bash
mktemp -d "solr.backup.$(date +%Y%m%d-%H%M%S).XXXXXX"
```

That produces something like `solr.backup.20261030-143052.a8Kp2z`: readable date and time, plus guaranteed uniqueness.

For the temporary `.solr-install.*` directory, the random suffix alone is sufficient because it disappears after installation.

## thet
