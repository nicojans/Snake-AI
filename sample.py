import ai
import snake
import numpy as np

STATE_SIZE = 8
ACTION_SIZE = 4


def play_easy():
    game = snake.Game(8, 8)
    game.play_new_game(12)


def play_normal():
    game = snake.Game(12, 12)
    game.play_new_game(8)


def play_hard():
    game = snake.Game(16, 16)
    game.play_new_game(4)


def train():
    episodes = 500
    steps = 1000
    game = snake.Game(10, 10)
    model = ai.Model(STATE_SIZE, ACTION_SIZE)

    for e in range(episodes):
        game.reset()
        tot_reward = 0
        for step in range(steps):
            state = game.state()
            previous_score = game.score
            action = model.act(state)
            alive = game.move(action)
            next_state = None
            reward = game.score - previous_score
            tot_reward += reward
            if alive:
                next_state = game.state()
            else:
                reward -= 1
            model.remember((state, action, reward, next_state))
            model.replay()
        print('Episode {}: score {}'.format(e + 1, game.score))

        if e % 50 == 49:
            scores = np.zeros(50)
            for i in range(50):
                game.reset()
                step = 0
                while step < steps:
                    if not game.move(model.act_best(game.state())):
                        break
                    step += 1
                scores[i] = game.score
            print('Average score on a new game: {}'.format(np.mean(scores)))

    model.save('model.h5')


def play_ai():
    game = snake.Game(10, 10)
    model = ai.Model(STATE_SIZE, ACTION_SIZE)
    model.load('model.h5')
    game.play_new_game(4, model.act_best)


play_ai()
