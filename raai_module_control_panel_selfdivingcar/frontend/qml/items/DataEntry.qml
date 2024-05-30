import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    id: entry
    property var databaseModel
//    property var dataList: ListModel {} // Create a ListModel
    property int entryWidth: 100 // Set a default entryWidth
    width: parent.width
    height: width / 20
    color: window.foreground_color
    border.width: 0

//    Component.onCompleted: {
//        // Populate the ListModel with data from dataModel
//        for (var key in databaseModel.keys) {
//            dataList.append({ "value": databaseModel.data[key] }); // Append the values
//        }
//    }

    Row {
        id: dataRow
        spacing: 5 // Adjust spacing as needed
        anchors.fill: parent

        Repeater {
            model: databaseModel.values

            delegate: Item {
                width: entryWidth
                height: parent.height

                Text {
                    text: modelData // Access the value from the model
//                    text: "hello"
                    anchors.centerIn: parent
                    color: lightFontColor
                }
            }
        }
    }
}
