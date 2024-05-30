import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle{

    id: custom_switch

    property string ontext: ""
    property string offtext: ""

    property color offcolor: "#ccc"
    property color oncolor: "#27ae60"
    property color textColor: '#F4EEE0'

    width: 60
    height: 30
    color: switchOn ? oncolor : offcolor
    radius: height / 2

    property bool switchOn: false

    Rectangle {
            id: circle

            y: parent.height/10

            height: parent.height - y*2
            width: height
            radius: width / 2
            border.width: 2
            border.color: "grey"
            color: "white"
            x: switchOn ? custom_switch.width - width - y : y
            smooth: true

            Behavior on x {
                NumberAnimation {
                    duration: 250
                }
            }
        }

    Text {
        text: switchOn ? ontext : offtext
        font.pixelSize: parent.height * 0.5
        anchors.centerIn: parent
        color: textColor
    }
}
