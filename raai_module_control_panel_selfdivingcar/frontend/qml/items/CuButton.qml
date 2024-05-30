import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Button {

    property string buttonText: ""
    property color bcolor: window.foreground_color
    property color border_color: window.accent_color
    property int radius_var: 3

    height: parent.height
    width: parent.width

    background: Rectangle{
        color: bcolor
        width: parent.width
        height: parent.height
        radius: radius_var
        border.width: 1
        border.color: border_color

        Text {
             text: buttonText
             color: window.lightFontColor
             anchors.centerIn: parent
        }
    }
}

