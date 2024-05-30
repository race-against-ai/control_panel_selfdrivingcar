import QtQuick 2.15
import QtQuick.Controls 2.15


Switch {
    id: control
        text: qsTr("Switch")
        width: container.width / 3
        height: width / 2

        indicator: Rectangle {
            implicitWidth: container.width / 3
            implicitHeight: width / 2
            y: parent.height / 2 - height / 2
            radius: 13
            color: control.checked ? window.dark_blue_text_color : "white"
            border.color: control.checked ? window.light_blue_text_color : "white"

            Rectangle {
                x: control.checked ? parent.width - width : 0
                width: height
                height: parent.height
                radius: 13
                color: control.down ? "grey" : "white"
                border.color: control.checked ? (control.down ? "grey" : "white") : "#999999"
            }
        }

    }


