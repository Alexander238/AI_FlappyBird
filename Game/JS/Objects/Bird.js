const imagePath = "../../Assets/bird.png";

const showHitboxes = false;


class Bird {
    constructor(canvas, context) {
        this.gameCanvas = canvas;
        this.x = 50;
        this.y = 100;
        this.velocity = 0;
        this.gravity = 4.5;
        this.lift = -350;

        this.birdImage = new Image();
        this.birdImage.src = imagePath;

        this.birdImage.onload = () => {
            this.imageWidth = this.birdImage.width / 10;
            this.imageHeight = this.birdImage.height / 10;

            this.width = this.birdImage.width / 10;
            this.height = this.birdImage.height / 10;
        };
    }

    update(deltaTime) {
        this.velocity += this.gravity;
        this.y += this.velocity * deltaTime;

        // Update hitboxes due to image
        this.leftHitboxX = this.x + 10;
        this.rightHitboxX = this.x + this.width - 10;
        this.bottomHitboxY = this.y + 5;
        this.topHitboxY = this.y + this.height - 5;

        // Limit bird's top position
        if (this.y < 0) {
            this.y = 0;
            this.velocity = 0;
        }

        // Limit bird's bottom position
        if (this.y + this.height> this.gameCanvas.height) {
            this.y = this.gameCanvas.height - this.height;
            this.velocity = 0;
        }
    }

    render(context) {
        if (showHitboxes) {
            context.fillStyle = "red";
            context.fillRect(this.leftHitboxX, this.bottomHitboxY, this.rightHitboxX - this.leftHitboxX, this.topHitboxY - this.bottomHitboxY);
        }
        context.save();
        context.translate(this.x + this.imageWidth / 2, this.y + this.imageHeight / 2);
        context.rotate(Math.PI / 6 * this.velocity / 500);
        context.drawImage(this.birdImage, -this.imageWidth / 2, -this.imageHeight / 2, this.imageWidth, this.imageHeight);
        context.restore();
    }

    flap() {
        this.velocity = this.lift;
    }
}

export { Bird };
