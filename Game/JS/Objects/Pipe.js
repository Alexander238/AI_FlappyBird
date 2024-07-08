class Pipe {
    constructor(canvas, isUpsideDown, speed = 25, width, length, upperY) {
        this.gameCanvas = canvas;
        this.isUpsideDown = isUpsideDown;
        this.x = this.gameCanvas.width;
        this.y = (upperY !== undefined ? upperY : 0)
        this.length = length;
        this.width = width;
        this.speed = speed;
    }

    update(deltaTime) {
        this.x -= this.speed * deltaTime;
    }

    render(context) {
        context.fillStyle = "green";

        if (this.isUpsideDown) {
            context.fillRect(this.x, this.y, this.width, this.length);
        } else {
            context.fillRect(this.x, this.y, this.width, this.length);
        }
    }

    isOffScreen() {
        return this.x + this.width < 0;
    }
}

export {Pipe};