import arcade
signal_seq = [[0, 35, 3, 154], [38, 35, 3, 116], [76, 89, 3, 24], [168, 21, 3, 0]]
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Traffic Signal"

class MyTimer(arcade.Window):
    def setup(self, sig):
        arcade.set_background_color(arcade.color.WHITE)
        self.i = 0
        self.total_time = sig[0]
        self.signal = sig.copy()

    def on_draw(self):
        arcade.start_render()
        if int(self.total_time) < 0:
            self.i += 1
            if self.i > 3:
                exit(0)
            self.total_time = int(self.signal[self.i])
        seconds = int(self.total_time)
        output = f"{seconds:02d}"

        if self.i == 0 or self.i == 3:
            img = arcade.load_texture('./images/red.png')
            arcade.draw_texture_rectangle(400, 300, 100, 250, img)
            arcade.draw_rectangle_filled(400, 145 , 100, 50, arcade.color.BLACK)
            arcade.draw_text(output, 380, 135, arcade.color.RED, 30)
        elif self.i == 1:
            img = arcade.load_texture('./images/green.png')
            arcade.draw_texture_rectangle(400, 300, 100, 250, img)
            arcade.draw_rectangle_filled(400, 145, 100, 50, arcade.color.BLACK)
            arcade.draw_text(output, 380, 135, arcade.color.GREEN, 30)
        elif self.i == 2:
            img = arcade.load_texture('./images/yellow.png')
            arcade.draw_texture_rectangle(400, 300, 100, 250, img)
            arcade.draw_rectangle_filled(400, 145, 100, 50, arcade.color.BLACK)
            arcade.draw_text(output, 380, 135, arcade.color.YELLOW, 30)

    def on_update(self, delta_time):
        self.total_time -= delta_time

"""def runArcade(i):
   # window = MyTimer()
    #window.setup(signal_seq[i])
    #arcade.run()
    print(i)"""

"""threads = []

for i in range(4):
    t = threading.Thread(target=runArcade, args=[i])
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()"""

window = MyTimer()
window.setup(signal_seq[0])
arcade.run()
window1 = MyTimer()
window1.setup(signal_seq[1])
arcade.run()
