class BattleAI {
    constructor(battleRoom) {
        this.battleRoom = battleRoom;
    }

    // Function to simulate receiving a request from the server
    receiveRequest(request) {
        console.log("AI received request:", request);

        // Decision making based on request type
        if (request.requestType === 'move') {
            this.makeMoveDecision(request);
        } else if (request.requestType === 'switch') {
            this.makeSwitchDecision(request);
        }
    }

    // Function to make a decision on which move to use
    makeMoveDecision(request) {
        // Simplified: Choose a random move
        const activePokemon = request.active[0]; // Assuming single battle for simplicity
        const moves = activePokemon.moves.filter(move => !move.disabled);
        const randomMove = moves[Math.floor(Math.random() * moves.length)];

        // Send decision back to the BattleRoom
        const decision = 'move ' + randomMove.id;
        console.log("AI decision:", decision);
        this.battleRoom.sendDecision(decision);
    }

    // Function to make a decision on which Pokemon to switch to
    makeSwitchDecision(request) {
        // Simplified: Choose a random switch option
        const switchOptions = request.side.pokemon.filter(pokemon => canSwitch(pokemon));
        const randomSwitch = switchOptions[Math.floor(Math.random() * switchOptions.length)];

        // Send decision back to the BattleRoom
        const decision = 'switch ' + randomSwitch.slot;
        console.log("AI decision:", decision);
        this.battleRoom.sendDecision(decision);
    }
}

// Helper function to check if a Pokémon can switch in
function canSwitch(pokemon) {
    return !pokemon.active && !pokemon.fainted;
}

// Mocking the BattleRoom's sendDecision function for this example
BattleRoom.prototype.sendDecision = function(decision) {
    console.log("Sending decision to server:", decision);
    // Here, you would normally interact with the server
};

// Example usage
const myBattleRoom = new BattleRoom(); // Assuming BattleRoom is already defined
const myBattleAI = new BattleAI(myBattleRoom);

// Simulate receiving a move request from the server
myBattleAI.receiveRequest({
    requestType: 'move',
    active: [{moves: [{id: 1, disabled: false}, {id: 2, disabled: false}]}]
});

// Simulate receiving a switch request from the server
myBattleAI.receiveRequest({
    requestType: 'switch',
    side: {
        pokemon: [
            {slot: 1, active: false, fainted: false},
            {slot: 2, active: true, fainted: false}, // Currently active
            {slot: 3, active: false, fainted: true}, // Fainted
            {slot: 4, active: false, fainted: false}
        ]
    }
});
