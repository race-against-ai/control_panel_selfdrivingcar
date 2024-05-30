import QtQuick 2.15

Item {
    id: wheel

    property real steering_value: 0

    Rectangle {
        color: "black"
        radius: 7.5
        height: car_image.height * 0.15
        width: car_image.width * 0.15
        rotation: wheel.steering_value * 0.5
    }
}
