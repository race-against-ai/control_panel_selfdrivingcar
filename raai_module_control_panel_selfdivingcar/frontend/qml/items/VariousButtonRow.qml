import QtQuick 2.15
import QtQuick.Controls 2.15

// various controls
Rectangle {
    height: 40
    color: controlBackground

    // used for changing the window state    
    ButtonWithBackground {
        x: 0
        y: 0
        height: 40
        width: 210

        buttonText: isFullScreen ? "FullScreen" : "Windowed"
        externalActivity: isFullScreen
        useExternalActivity: true

        onButtonClicked: function() {
            isFullScreen = !isFullScreen

            if(isFullScreen) {
                window.visibility = "FullScreen"
            } else {
                window.visibility = "Windowed"
            }
        }
    }

    // disable or enable buttons on the steering wheel
    ButtonWithBackground {
        x: 210
        y: 0
        height: 40
        width: 210

        buttonText: control_panel_model.start_status ? "Start active" : "Start inactive"
        externalActivity: control_panel_model.start_status
        useExternalActivity: true

        onButtonClicked: function() {
            buttonStartStatusChanged()
        }
    }

    // enable or disable the platform
    ButtonWithBackground {
        x: 420
        y: 0
        height: 40
        width: 210

        buttonText: control_panel_model.stream_status ? "Stream active" : "Stream inactive"
        externalActivity: control_panel_model.stream_status
        useExternalActivity: true

        onButtonClicked: function() {
            buttonStreamStatusChanged()
        }
    }

    ButtonWithBackground {
        x: 630
        y: 0
        height: 40
        width: 210

        buttonText: control_panel_model.motor_status ? "motor active" : "motor inactive"
        externalActivity: control_panel_model.motor_status
        useExternalActivity: true

        onButtonClicked: function() {
            buttonMotorStatusChanged()
        }
    }

    ButtonWithBackground {
        x: 840
        y: 0
        height: 40
        width: 210

        buttonText: control_panel.debug_status ? "debug active" : "debug inactive"
        externalActivity: control_panel_model.debug_status
        useExternalActivity: true

        onButtonClicked: function() {
            buttonDebugStatusChanged()
        }
    }

    ButtonWithBackground {
        x: 1050
        y: 0
        height: 40
        width: 210

        buttonText: control_panel_model.process_status ? "Process active" : "Process inactive"
        externalActivity: control_panel_model.process_status
        useExternalActivity: true

        onButtonClicked: function() {
            buttonProcessStatusChanged()
        }
    }
}
