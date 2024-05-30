import QtQuick 2.0

Rectangle {
    property bool isActive

    property string activeColour: "#00FF00"
    property string inactiveColour: "#FF0000"

    color: {
        if(isActive) {
            activeColour
        } else {
            inactiveColour
        }
    }

    border.color: "#000000"
}
