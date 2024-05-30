import QtQuick 2.15
import QtQuick.Controls 2.15

Rectangle {
    height: 40
    color: controlBackground

    Rectangle {
        x: 0
        y: 0
        width: 210
        height: 40

        color: controlBackground
        border.color: "#000000"
    }
    Rectangle {
        x: 5
        y: 5
        height: 30
        width: 200

        border.color: "#000000"
        border.width: 2
        color: barForeground
    }
    Text {
        text: "timer controls:"
        x: 5
        y: 5
        height: 30
        width: 200
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter

        font.family: "Consolas"
        font.pixelSize: 20
    }

    ButtonWithBackground {
        x: 210
        y: 0
        height: parent.height
        width: 210

        buttonText: "start"
        invertActivity: true

        onButtonClicked: function() {
            timerStart()
        }
    }

    ButtonWithBackground {
        x: 420
        y: 0
        height: parent.height
        width: 210

        buttonText: "pause"
        invertActivity: true

        onButtonClicked: function() {
            timerPause()
        }
    }

    ButtonWithBackground {
        x: 630
        y: 0
        height: parent.height
        width: 210

        buttonText: "stop"
        invertActivity: true

        onButtonClicked: function() {
            timerStop()
        }
    }

    ButtonWithBackground {
        x: 840
        y: 0
        height: parent.height
        width: 210

        buttonText: "reset"
        invertActivity: true

        onButtonClicked: function() {
            timerReset()
        }
    }

    ButtonWithBackground {
        x: 1050
        y: 0
        height: parent.height
        width: 210

        buttonText: "full reset"
        invertActivity: true

        onButtonClicked: function() {
            timerResetFull()
        }
    }

    ButtonWithBackground {
        x: 1260
        y: 0
        height: parent.height
        width: 210

        buttonText: "ignore"
        invertActivity: true

        onButtonClicked: function() {
            timerIgnore()
        }
    }
}
