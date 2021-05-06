const getGeneralMsg = new WebSocket("ws://" + window.location.host + "/ws/all/");

getGeneralMsg.onmessage = function(e) {
    alert(e.data);
};

getGeneralMsg.onopen = function (event){
    getGeneralMsg.send(document.cookie.split(";")[1].replace(" ", "").split("=")[1]);
};
