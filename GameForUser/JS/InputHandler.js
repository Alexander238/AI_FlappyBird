class InputHandler {
    constructor(bird) {
        this.bird = bird;

        this.addEventListener();
    }

    flapBird() {
        this.bird.flap();
    }

    addEventListener() {
        window.addEventListener("keydown", (event) => {
            if (event.code === "Space") {
                this.flapBird();
            }
        });
    }
}

export {InputHandler};