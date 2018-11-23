import tensorflow as tf
import ai
import snake
import matplotlib.pylab as plt
import numpy as np


WIDTH = 10
HEIGHT = 10
SPEED = 10

game = snake.Game(WIDTH, HEIGHT)
#aaaa = gamescreen.play(game, 30)
#exit(1)
BATCH_SIZE = 50
num_states = 9
num_actions = 4

model = ai.Model(num_states, num_actions, BATCH_SIZE)
mem = ai.Memory(50000)
saver = tf.train.Saver()


with tf.Session() as sess:
    sess.run(model.var_init)
    gr = ai.GameRunner(sess, model, game, mem)
    num_episodes = 300
    cnt = 0
    while cnt < num_episodes:
        if cnt % 50 == 0:
            print('Episode {} of {}'.format(cnt+1, num_episodes))
            tot_score = 0
            for i in range(50):
                game.reset()
                step = 0
                while step < 500:
                    if not game.move(np.argmax(model.predict_one(game.state(), sess))):
                        break
                    step += 1
                tot_score += game.score

            print(tot_score / 50)

        gr.run()
        cnt += 1

    save_path = saver.save(sess, "C:/test/model.ckpt")

    tot = 0
    scores = []
    for i in range(len(gr.score_store)):
        tot += gr.score_store[i]
        if i % 20 == 19:
            scores += [tot / 20]
            tot = 0

    plt.plot(scores)
    plt.show()

    computer = ai.AiController(game, model, sess)
    game.play_new_game(5, computer)


