from vispy import app, scene
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout
import numpy as np

class LivePlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Live Plot")
        self.setGeometry(100, 100, 800, 600)

        layout = QHBoxLayout()
        self.setLayout(layout)

        self.canvas = scene.SceneCanvas(keys='interactive', size=(800, 400))
        layout.addWidget(self.canvas.native)

        grid = self.canvas.central_widget.add_grid(margin=0)
        grid.spacing = 0
        grid.border_color = 'white'

        # Title
        title = scene.Label("Live View", color='white')
        title.height_max = 40
        grid.add_widget(title, row=0, col=0, col_span=2)

        # Y Axis (left)
        yaxis = scene.AxisWidget(
            orientation='left',
            axis_label='Y Axis',
            axis_font_size=12,
            axis_label_margin=50,
            tick_label_margin=5,
        )

        yaxis.width_max = 80
        yaxis.border_color = 'white'
        grid.add_widget(yaxis, row=1, col=0)

        # View (main plot)
        self.view = grid.add_view(row=1, col=1)
        self.view.camera = 'panzoom'
        self.view.border_color = 'white'
        yaxis.link_view(self.view)

        scene.visuals.GridLines(parent=self.view.scene)

        # Line plot
        self.line = scene.Line(np.array([[0, 0]]), width = 2 , parent=self.view.scene)
        self.view.camera.set_range(x=(1000, 10000), y=(-100000, 100000))

        # processed data line  plot 
        self.processed_line = scene.Line(np.array([[0,0]]) , color="magenta" , width= 2 , parent= self.view.scene)
        self.processed_line_visible = False 

    def update_data(self, time_axis, data):
        #print("Updating data in LivePlotWidget")
        line_data = np.column_stack((time_axis, data))
        self.line.set_data(line_data)
        self.canvas.update()

    def update_processed_data(self , time_axis , data):
        #print("Updating processed data in LivePlotWidget")
        line_data  = np.column_stack((time_axis , data))
        self.processed_line.set_data(line_data)
        self.canvas.update()

    def set_display_mode(self, mode):
        """Toggle between raw and processed views"""
        self.line.visible = (mode == 'raw')
        self.processed_line.visible = (mode != 'raw')
        
        # Update colors based on mode
        colors = {
            'rms': (1, 0.5, 0, 1),    # Orange
            'envelope': (0, 1, 0, 1), # Green
            'filtered': (1, 0, 1, 1)   # Magenta
        }
        #self.processed_line.color = colors.get(mode, (1, 0, 1, 1))
        self.canvas.update()


