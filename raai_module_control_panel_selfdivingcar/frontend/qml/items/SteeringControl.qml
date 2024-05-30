import QtQuick 2.0
import QtQuick.Controls 2.15

Rectangle {
	id: steeringControl

    signal sliderMaxChanged(val: real)
    signal sliderSteeringOffsetChanged(val: real)

	property real value: 0
	property real actualValue: 0
	property real maxValue: 0
    property real steeringOffset: 0

	property color barBackground
    property color barForeground

	// all controls (throttle, brake, clutch, and steering wheel) have two rectangles:
	// the first one is for the actual value
	// the second is for the used value

	// if the slider value is above 100, the function of the recatngle is switched
	// then the background rectangle is for showing the used and the front one is for the actual value
	Rectangle {
        x: {
            if(steering_slider.value > 100) {
                if(control_panel_model.actual_steering > 0) {
                    (parent.width / 2) - ((parent.width / 2 - 10) * (Math.abs(steeringControl.actualValue) / 100)) * (steering_slider.value / 100)
                } else {
                    (parent.width / 2)
                }
            } else {
                if(control_panel_model.actual_steering > 0) {
                    (parent.width / 2) - ((parent.width / 2 - 10) * (Math.abs(steeringControl.actualValue) / 100))
                } else {
                    (parent.width / 2)
                }
            }
        }
		y: 10

		color: barBackground

        height: barHeight
		width: {
			if(steering_slider.value > 100) {
                (parent.width / 2 - 10) * (Math.abs(steeringControl.value) / 100)
			} else {
                (parent.width / 2 - 10) * (Math.abs(steeringControl.actualValue) / 100)
			}
		}
	}

	Rectangle {
		x: {
            if(steering_slider.value > 100) {
                if(steeringControl.actualValue > 0) {
                    (parent.width / 2) - ((parent.width / 2 - 10) * (Math.abs(steeringControl.actualValue) / 100))
                } else {
                    (parent.width / 2)
                }
			} else {
                if(steeringControl.actualValue > 0) {
					(parent.width / 2) - ((parent.width / 2 - 10) * (Math.abs(steeringControl.value) / 100))
				} else {
					(parent.width / 2)
				}
			}
		}
		y: 10

		color: barForeground

        height: barHeight
		width: {
			if(steering_slider.value > 100) {
				(parent.width / 2 - 10) * (Math.abs(steeringControl.actualValue) / 100)
			} else {
				(parent.width / 2 - 10) * (Math.abs(steeringControl.value) / 100)
			}
		}
	}

	Text {
		x: 20
		y: 10
		text: String(steeringControl.value.toFixed(postComma)).padStart(numLength, " ")
		font.family: "Consolas"
		font.bold: true
		font.pointSize: fontNumberSize
	}

	Text {
		x: parent.width - 20 - this.width
		y: 10
		text: String(steeringControl.actualValue.toFixed(postComma)).padStart(numLength, " ")
		font.family: "Consolas"
		font.bold: true
		font.pointSize: fontNumberSize
	}

	Text {
		x: 260
		y: 10
		text: "steering"
		font.pointSize: fontDescriptionSize
		anchors.horizontalCenter: parent.horizontalCenter
		font.family: "Consolas"
		font.bold: true
	}

	Slider {
		id: steering_slider
		x: 10
		y: 50

		height: 40
		width: parent.width - 20

		from: 0
		to: 200
		value: steeringControl.maxValue

        onMoved: steeringControl.sliderMaxChanged(value)

		Text {
			y: -10
			text: parent.value.toFixed(postComma) + "%"
			anchors.horizontalCenter: parent.horizontalCenter
			font.family: "Consolas"
			font.bold: true
			font.pointSize: fontSliderSize
		}
	}
    Slider {
        id: steeringOffsetSlider
        x: 10
        y: 90

        height: 40
        width: parent.width - 20

        // inversion, as + is left and - is right
        from: 100
        to: -100
        value: steeringControl.steeringOffset

        onMoved: steeringControl.sliderSteeringOffsetChanged(value)

        Text {
            y: -10
            text: parent.value.toFixed(postComma)
            anchors.horizontalCenter: parent.horizontalCenter
            font.family: "Consolas"
            font.bold: true
            font.pointSize: fontSliderSize
        }
    }
}
