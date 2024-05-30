import QtQuick 2.0
import QtQuick.Controls 2.15

Rectangle {
    id: pedalControl

    signal sliderMaxChanged(val: real)

    property string title

    property real value: 0
    property real actualValue: 0
    property real maxValue: 0

    property color barBackground
    property color barForeground

    // all controls (throttle, brake, clutch, and steering wheel) have two rectangles:
    // the first one is for the actual value
    // the second is for the used value

    Rectangle {
        x: 10
        y: 10

        color: parent.barBackground

        height: barHeight
        width: (parent.width - 20) * (Math.abs(pedalControl.actualValue) / 100)
    }

    Rectangle {
        x: 10
        y: 10

        color: parent.barForeground

        height: barHeight
        width: (parent.width - 20) * (Math.abs(pedalControl.value) / 100)
    }

    Text {
        x: 20
        y: 10
        text: String(pedalControl.value.toFixed(postComma)).padStart(numLength, " ")
        font.family: "Consolas"
        font.bold: true
        font.pointSize: fontNumberSize
    }

    Text {
        x: parent.width - 20 - this.width
        y: 10
        text: String(pedalControl.actualValue.toFixed(postComma)).padStart(numLength, " ")
        font.family: "Consolas"
        font.bold: true
        font.pointSize: fontNumberSize
    }

    Text {
        x: 260
        y: 10
        text: pedalControl.title
        anchors.horizontalCenter: parent.horizontalCenter
        font.family: "Consolas"
        font.bold: true
        font.pointSize: fontDescriptionSize
    }

    Slider {
        x: 10
        y: 50

        height: 40
        width: parent.width - 20

        from: 0
        to: 100
        value: pedalControl.maxValue

        onMoved: pedalControl.sliderMaxChanged(value)

        Text {
            y: -10
            text: parent.value.toFixed(2) + "%"
            anchors.horizontalCenter: parent.horizontalCenter
            font.family: "Consolas"
            font.bold: true
            font.pointSize: fontSliderSize
        }
    }
}
