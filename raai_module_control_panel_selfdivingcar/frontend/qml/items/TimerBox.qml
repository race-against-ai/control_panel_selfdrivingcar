import QtQuick 2.0
import QtQuick.Controls 2.15

Item {
    Rectangle {
        radius: 20
        color: window.light_grey
        height: parent.height
        width: parent.width
        border.color: "white"
        border.width: 5

        Text {
            id: control
            text: "Timer"
            color: window.dark_blue_text_color
            font.bold: true
            anchors.horizontalCenter: parent.horizontalCenter
            y: parent.height * 0.01
            font.pointSize: parent.width * 0.15
        }

        Item {
            id: container
            width: parent.width
            height: parent.height * 0.6
            anchors.verticalCenter: parent.verticalCenter

            VariousButton {
                y: 0
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Start"
                width: parent.width * 0.7
                height: parent.height * 0.15


                onClicked: function() {
                    timerStart()
                }
            }

            VariousButton {
                y: parent.height * 1 / 4
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Pause"
                width: parent.width * 0.7
                height: parent.height * 0.15

                onClicked: function() {
                    timerPause()
                }
            }

            VariousButton {
                y: parent.height * 2 / 4
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Reset"
                width: parent.width * 0.7
                height: parent.height * 0.15

                onClicked: function() {
                    timerReset()
                }
            }

            VariousButton {
                y: parent.height * 3 / 4
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Ignore"
                width: parent.width * 0.7
                height: parent.height * 0.15

                onClicked: function() {
                    timerIgnore()
                }
            }

            VariousButton {
                id: mode_button
                y: parent.height * 4 / 4
                anchors.horizontalCenter: parent.horizontalCenter
                text: "Darkmode"
                width: parent.width * 0.7
                height: parent.height * 0.15

                onClicked: {
                    if (mode_button.text === "Darkmode") {
                        mode_button.text = "Lightmode"
                        window.background_color_start_light =  "#3a414f"
                        window.background_color_stop_light = "#1a1d24"
                        window.light_grey = "#bfbfbf"
                        window.light_grey = "#757575"
                        window.caption_text_color = "#7ba4e3"

                    } else {
                        mode_button.text = "Darkmode"
                        window.background_color_start_light = "#e1e8f5"
                        window.background_color_stop_light = "#a5acb8"
                        window.light_grey = "#bfbfbf"
                        window.caption_text_color = "#274c87"
                    }
                }
            }


        }
    }
}
