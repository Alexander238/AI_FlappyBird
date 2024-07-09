const imagePath = "../../Assets/bird.png";

const showHitboxes = true;


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
            this.width = this.birdImage.width / 10;
            this.height = this.birdImage.height / 10;
        };
    }

    update(deltaTime) {
        this.velocity += this.gravity;
        this.y += this.velocity * deltaTime;

        // Update hitboxes due to image
        this.rightHitboxX = this.x + 10;
        this.leftHitboxX = this.x + this.width - 10;
        this.bottomHitboxY = this.y + 5;
        this.topRightHitboxY = this.y + this.height - 5;

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
            context.fillRect(this.rightHitboxX, this.bottomHitboxY, this.leftHitboxX - this.rightHitboxX, this.topRightHitboxY - this.bottomHitboxY);

            context.fillStyle = "blue";
            // draw big blue circles at the corners of the hitbox
            context.beginPath();
            context.arc(this.rightHitboxX, this.bottomHitboxY, 5, 0, 2 * Math.PI);
            context.fill();

            context.fillStyle = "red";
            context.beginPath();
            context.arc(this.leftHitboxX, this.bottomHitboxY, 5, 0, 2 * Math.PI);
            context.fill();

            context.fillStyle = "green";
            context.beginPath();
            context.arc(this.rightHitboxX, this.topRightHitboxY, 5, 0, 2 * Math.PI);
            context.fill();

            context.fillStyle = "black";
            context.beginPath();
            context.arc(this.leftHitboxX, this.topRightHitboxY, 5, 0, 2 * Math.PI);
            context.fill();

        }
        context.save();
        context.translate(this.x + this.width / 2, this.y + this.height / 2);
        context.rotate(Math.PI / 6 * this.velocity / 500);
        context.drawImage(this.birdImage, -this.width / 2, -this.height / 2, this.width, this.height);
        context.restore();
    }

    flap() {
        this.velocity = this.lift;
    }
}

export { Bird };
