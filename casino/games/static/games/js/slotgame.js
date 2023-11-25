Array.prototype.sample = function(){
    return this[Math.floor(Math.random()*this.length)];
}

// CONSTANTS

const user = "TestUser";
const patterns = [1,1,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4];
const baseMultiplier = 6;


// USER DATA

let balance = 500;


// SPIN

let spin = (bet) => {
    winning_numbers = [patterns.sample(),patterns.sample(),patterns.sample()];
    if (winning_numbers[0] === winning_numbers[1] && winning_numbers[0] === winning_numbers[2]) {
        return bet * (baseMultiplier-winning_numbers[0])
    }else{
        return 0
    }
}

// MACHINE

current_bet = 20
let play = true

let machine = (user) => {
    while (play) {
        if ((balance - current_bet) < 0){
            break
        }
        balance -= current_bet
        win = spin(current_bet)
        balance += win
        console.log(balance)

    }
}

machine()

