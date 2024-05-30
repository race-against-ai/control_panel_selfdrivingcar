// Copyright (C) 2023 NGITL
import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15

Flickable {
    property var databaseModel
    id: flickableData
    width: parent.width
    height: parent.height
    contentWidth: rowOfTexts.totalWidth
    contentHeight: data_rect.height
    anchors.top: filler_rect_2.bottom

    clip: true

    Rectangle{
        id: data_rect
        color: "transparent"
        width: Math.max(rowOfTexts.totalWidth, window.width) // Use dynamicWidth property
        height: parent.parent.height

        Rectangle {
            id: data_keys
            width: Math.max(rowOfTexts.totalWidth, window.width)
            height: parent.height * 0.08
            anchors.top: parent.top
            color: foreground_color

            Row {
                id: rowOfTexts
                spacing: 5 // Adjust spacing as needed
                anchors.fill: parent
                property int totalWidth: window.entry_width * database.keyAmount

                Repeater {
                    model: database.database_keys
                    delegate: Item {
                        width: window.entry_width
                        height: parent.height

                        Text {
                            text: modelData.key
                            anchors.centerIn: parent
                            color: lightFontColor
                        }

                    }
                }
            }
        }

        Rectangle {
            width: parent.width
            height: parent.height - data_keys.height - 6
            anchors.bottom: parent.bottom
            color: "transparent"
            ScrollView {
                id: scrollView
                anchors.fill: parent
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                ScrollBar.vertical: ScrollBar{
                    id: scrollBar

                    hoverEnabled: true
                    policy: ScrollBar.AsNeeded
                    width: 6

                    parent: scrollView.parent
                    x: scrollView.mirrored ? 0 : scrollView.width - width
                    height: scrollView.availableHeight
                    opacity: 0

                    background: Rectangle {
                        color: foreground_color
                    }
                }

                Column {
                    id: column
                    anchors.fill: parent
                    spacing: 3

                    Repeater {
                        id: data_repeater
                        model: databaseModel.data

                        delegate: DataEntry {
                            databaseModel: modelData
                            width: data_rect.width
                            entryWidth: window.entry_width
                            height: data_rect.height/12.5
                        }
                    }
                }
            }
        }
    }
    ScrollBar.horizontal: ScrollBar {
        width: 6
        policy: ScrollBar.AsNeeded
    }
}
