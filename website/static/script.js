const CONFIGURATION = {
    "locations": [
    {"title":"CNR, Istituto di Scienze Polari, edificio Delta",
    "address1":"Via Torino",
    "address2":"155, 30172 Venezia VE, Italy",
    "coords":{"lat":45.47789406868193,"lng":12.25580353558198}}
    ,{"title":"edificio Zeta","address1":"Via Torino","address2":"155, 30172 Venezia VE, Italy","coords":{"lat":45.47860446275129,"lng":12.25596107578409}}
    ],
    "mapOptions": {"center":{"lat":45.47885712419216,"lng":12.25533016940596},"fullscreenControl":false,"mapTypeControl":true,"streetViewControl":false,"zoom":13,"zoomControl":true,"maxZoom":20,"mapId":""},
    "mapsApiKey": "AIzaSyBbfyIpvNetPbX4UGtv6ddVjprg4cMA9vo",
    "capabilities": {"input":true,"autocomplete":true,"directions":false,"distanceMatrix":true,"details":false,"actions":true}
};

function initMap() {
    new LocatorPlus(CONFIGURATION);
}