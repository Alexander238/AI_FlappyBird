const pipeHeadPath = "../../Assets/pipe_head.png";
const pipeBodyPath = "../../Assets/pipe_body.png";

const showHitboxes = true;

class Pipe {
    constructor(canvas, isUpsideDown, speed = 25, length, upperY) {
        this.gameCanvas = canvas;
        this.isUpsideDown = isUpsideDown;
        this.x = this.gameCanvas.width;
        this.y = (upperY !== undefined ? upperY : 0)
        this.length = length;
        this.speed = speed;

        this.pipeHead = new Image();
        this.pipeHead.src = pipeHeadPath;
        this.pipeHead.onload = () => {
            this.headWidth = this.pipeHead.width / 10;
            this.headHeight = this.pipeHead.height / 10;
        };

        this.pipeBody = new Image();
        this.pipeBody.src = pipeBodyPath;
        this.pipeBody.onload = () => {
            this.bodyWidth = this.pipeBody.width / 10;
            this.bodyHeight = this.pipeBody.height / 10;
        };

        this.updateHitboxes();
    }

    update(deltaTime) {
        this.x -= this.speed * deltaTime;
        this.updateHitboxes();
    }

    updateHitboxes() {
        this.bodyRightX = this.x + 7;
        this.bodyLeftX = this.x + this.bodyWidth - 7;
        this.bodyBottomY = this.y;
        this.bodyTopY = this.y + this.length;

        if (this.isUpsideDown) {
            this.headRightX = this.x;
            this.headLeftX = this.x + this.headWidth;
            this.headBottomY = this.y + this.length;
            this.headTopY = this.y + this.length + this.headHeight;
        } else {
            this.headRightX = this.x;
            this.headLeftX = this.x + this.headWidth;
            this.headBottomY = this.y - this.headHeight;
            this.headTopY = this.y;
        }

    }

    render(context) {
        if (showHitboxes) {
            context.fillStyle = "red";
            context.fillRect(this.bodyRightX, this.bodyBottomY, this.bodyLeftX - this.bodyRightX, this.bodyTopY - this.bodyBottomY);
            context.fillStyle = "blue";
            context.fillRect(this.headRightX, this.headBottomY, this.headLeftX - this.headRightX, this.headTopY - this.headBottomY);

            // draw big blue circles at the corners of the hitbox
            context.fillStyle = "blue";
            context.beginPath();
            context.arc(this.headRightX, this.headBottomY, 5, 0, 2 * Math.PI);
            context.fill();

            context.fillStyle = "red";
            context.beginPath();
            context.arc(this.headLeftX, this.headBottomY, 5, 0, 2 * Math.PI);
            context.fill();

            context.fillStyle = "green";
            context.beginPath();
            context.arc(this.headRightX, this.headTopY, 5, 0, 2 * Math.PI);
            context.fill();

            context.fillStyle = "black";
            context.beginPath();
            context.arc(this.headLeftX, this.headTopY, 5, 0, 2 * Math.PI);
            context.fill();

        }

        if (this.pipeBody.complete && this.pipeHead.complete) {
            if (this.isUpsideDown) {
                let yOffset = this.y;
                while (yOffset < this.y + this.length) {
                    context.drawImage(this.pipeBody, this.x, yOffset, this.bodyWidth, this.bodyHeight);
                    yOffset += this.bodyHeight;
                }
                context.drawImage(this.pipeHead, this.x, this.y + this.length, this.headWidth, this.headHeight);
            } else {
                let yOffset = this.y;
                while (yOffset < this.y + this.length) {
                    context.drawImage(this.pipeBody, this.x, yOffset, this.bodyWidth, this.bodyHeight);
                    yOffset += this.bodyHeight;
                }
                context.drawImage(this.pipeHead, this.x, this.y - this.headHeight, this.headWidth, this.headHeight);
            }
        }
    }

    isOffScreen() {
        return this.x + this.width < 0;
    }
}

export {Pipe};