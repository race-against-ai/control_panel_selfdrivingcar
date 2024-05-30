import QtQuick 2.15
import QtQuick.Controls 2.15

import "./../items"

Item {
    signal navigateBack()

    anchors.fill: parent

    Rectangle {
        id: background
        anchors.fill: parent
        gradient: Gradient {
            orientation: Gradient.Horizontal
            GradientStop {
                position: 0.0
                color: background_color_start_light
            }
            GradientStop {
                position: 1.0
                color: background_color_stop_light
            }
        }
        Component.onCompleted: {
            console.log("Background created");
        }
    }

    Column {
        spacing: 5
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.margins: 20

        Label {
            text: "Enter the name:"
            font.pixelSize: 20
            font.bold: true
        }

        TextField {
            id: driverEntry
            width: 400
            font.pixelSize: 18
            padding: 10
            background: Rectangle {
                color: "lightgrey"
                radius: 10
            }
        }

        Row {
            spacing: 20

            Button {
                text: "Search"
                onClicked: database_model.search_driver(driverEntry.text)
                font.pixelSize: 18
                padding: 10
            }

            Button {
                text: "Create"
                onClicked: database_model.create_driver(driverEntry.text)
                font.pixelSize: 18
                padding: 10
            }

            Button {
            text: "Debug: Send"
            onClicked: database_model.send_data(driverEntry.text)
            font.pixelSize: 18
            padding: 10
        }

            Button {
                text: "Refresh"
                onClicked: database_model.refresh_driver()
                font.pixelSize: 18
                padding: 10
            }
        } 
    }

    Rectangle {
    id: content
    color: "#f0f0f0"
    anchors.centerIn: parent
    width: parent.width * 0.9
    height: parent.height * 0.65
    radius: 10

        ScrollView {
            id: scrollView
            anchors.fill: parent
            clip: true
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            Column {
                width: scrollView.width
                spacing: 5

                Repeater {
                    model: database_model.drivers

                    delegate: Rectangle {
                        width: content.width
                        height: content.height / 15
                        opacity: mouseHandler.containsMouse ? 1 : 0.5
                        color: index % 2 === 0 ? "#ffffff" : "#e0e0e0"
                        radius: 5

                        Row {
                            anchors.fill: parent
                            spacing: 10

                            MouseArea {
                                id: mouseHandler
                                anchors.fill: parent
                                hoverEnabled: true
                                onClicked: database_model.send_data(modelData.name)
                            }

                            Text {
                                color: "black"
                                text: modelData.name
                                anchors.verticalCenter: parent.verticalCenter
                                font.pixelSize: 16
                            }

                            Text {
                                color: "black"
                                text: modelData.created
                                anchors.horizontalCenter: parent.horizontalCenter
                                anchors.verticalCenter: parent.verticalCenter
                                font.pixelSize: 16
                            }

                            Text {
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                color: "black"
                                text: modelData.id
                                font.pixelSize: 16
                            }
                        }
                    }
                }
            }
        }
    }

    Text {
            text: "Status: " + database_model.status
            font.pixelSize: 18
            anchors.horizontalCenter: parent.horizontalCenter
            y: parent.height * 0.9
    }
}
