import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs

Rectangle{
    id: title_bar

    width: parent.width
    height: parent.height

    color: window.foreground_color

    Rectangle{
        id: upper_part
        width: parent.width - parent.height/6
        color: 'transparent'
        anchors.left: parent.left
        height: parent.height

        Text {
            id: title
            text: "Database"
            color: window.lightFontColor
            font.pointSize: parent.height/2
            leftPadding: height/6
            wrapMode: Text.Wrap

            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
        }

    }
}
