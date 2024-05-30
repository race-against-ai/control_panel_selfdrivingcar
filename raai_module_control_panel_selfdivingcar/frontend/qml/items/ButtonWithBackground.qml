import QtQuick 2.15
import QtQuick.Controls 2.15

Item {
    id: background

    property string activeColour: "#00FF00"
    property string inactiveColour: "#FF0000"
    property string buttonText: ""
    property string fontType: "Consolas"

    property int buttonPadding: 5
    property int fontSize: 20

    property bool invertActivity: false
    property bool externalActivity
    property bool useExternalActivity: false

    signal buttonClicked

    ButtonBackground {
        x: 0
        y: 0
        width: parent.width
        height: parent.height

        activeColour: activeColour
        inactiveColour: inactiveColour

        isActive: {
            // an external status has been set, use it
            // testing for it being set is useless, as it will default to a boolean
            if(useExternalActivity) {
                externalActivity
            // otherwise use the button
            // (and invert it if necessary)
            } else invertActivity ? !button.pressed : button.pressed
        }

    }
    Button {
        id: button
        x: buttonPadding
        y: buttonPadding
        height: background.height - (2 * buttonPadding)
        width: background.width - (2 * buttonPadding)

        text: buttonText
        font.family: fontType
        font.pixelSize: fontSize

        onClicked: buttonClicked()
    }
}
