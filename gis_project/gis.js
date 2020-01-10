
var tmpl = '<div style="font-family: dotum, arial, sans-serif;font-size: 18px;' +
'font-weight: bold;margin-bottom: 5px;">#{name}</div>' +
'<table style="border-spacing: 2px; border: 0px"><tbody><tr>' +
'<tr><td style="color:#767676;padding-right:12px">주소</td>' +
'<td><span>#{address}</span></td></tr>' +
'<tr><td style="color:#767676;padding-right:12px">거리</td>' +
'<td style=""><span>#{dist} m</span></td></tr>' +
'<tr><td style="color:#767676;padding-right:12px">평점</td>' +
'<td style=""><span>#{rate}/5 점</span></td></tr>' +
'</tr></tbody></table>';
var map;
var info = new olleh.maps.overlay.InfoWindow({
position: new olleh.maps.UTMK(953823.7, 1953435.52),
maxWidth: 400,
//content: olleh.maps.util.applyTemplate(tmpl, data),
pixelOffset: new olleh.maps.Point(0, -40) //marker.getIcon().size.height
});
var markers = [];
var me = new olleh.maps.UTMK(965991.8348, 1929032.7373);
var salonRawData = [[37.358812, 127.119542, "건영미용실", 3], [37.360405, 127.113182, "지수미용실", 5], 
    [37.360934, 127.117158, "민조미용실", 5], [37.355449, 127.112655, "진아미용실", 5], 
    [37.350954, 127.110495, "조금먼미용실", 4], [37.350355, 127.111371, "조금먼미용실2", 3],
    [37.403994, 127.116062, "조금먼미용실3", 2], [37.257466, 127.140421, "조금먼미용실4", 3],
    [37.298026, 126.972356, "먼미용실", 4], [37.263255, 127.108309, "먼미용실", 3.5],
    [36.337849, 127.393417, "대전미용실", 5], [35.160223, 129.165114, "부산미용실", 5]]
var salonData = []
function initialize() {
    me = new olleh.maps.UTMK(965991.8348, 1929032.7373);
    var mapOpts = {
        center: me,
        zoom: 11,
        mapTypeId: 'ROADMAP'
    };
    map = new olleh.maps.Map(document.getElementById('map_div'), mapOpts);
    getData();
}


function latlngToUtmk(x, y){ 
    let p = olleh.maps.UTMK.valueOf(new olleh.maps.LatLng(x, y))
    return p
}

window.onload = initialize;

function getData(){
// 기존의 marker 들을 지워주는 코드
    markers.some((_element, _index, _array) =>{
    markers[_index].setVisible(false);
    });
    markers = []
    salonData = []
    salonRawData.some((_element, _index, _array) => {
    let tmp_pos = latlngToUtmk(_element[0], _element[1]);
    salonData.push(tmp_pos);
    dist = tmp_pos.distanceTo(me);
    if (dist <= 1000) {
        let marker = new olleh.maps.overlay.Marker({
            position: tmp_pos,
            map: map,
            caption: "미용실"
        });
        marker['attribute'] = {"name":_element[2], "dist": parseInt(dist), "rate": _element[3]};
        marker.onEvent('click', function(e) {
            infoWindowShow(this);
        });
        markers.push(marker);
    }
    });
    me = new olleh.maps.UTMK(1151654.8847289516, 1686265.631509801);
}

function infoWindowShow(marker){
    info.setContent(olleh.maps.util.applyTemplate(tmpl, marker.attribute))
    info.setPosition(marker.getPosition())
    console.log(map);
    info.open(map)
}
