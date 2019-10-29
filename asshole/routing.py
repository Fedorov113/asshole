from channels.routing import ProtocolTypeRouter, URLRouter
import explorer.routing

application = ProtocolTypeRouter({
    'http': URLRouter(explorer.routing.urlpatterns),
})