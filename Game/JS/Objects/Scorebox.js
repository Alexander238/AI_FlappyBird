class Scorebox {
    constructor(context) {
        this.context = context;
        this.score = 0;
    }

    render(context) {
        context.font = "30px Arial";
        context.fillStyle = "black";
        context.fillText(`Score: ${this.score}`, 10, 30);
    }

    incrementScore() {
        this.score++;
    }

    getScore() {
        return this.score;
    }

    reset(){
        this.score = 0;
    }
}

export { Scorebox };