class InputHandler {
    constructor(bird) {
        this.bird = bird;

        this.addEventListener();
    }

    addEventListener() {
        window.addEventListener("keydown", (event) => {
            if (event.code === "Space") {
                this.bird.flap();
            }
        });
    }
}

export {InputHandler};