import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.colorchooser.*;
import java.lang.Runtime;
import java.io.File;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;

/* RGB_Controller.java requires no other files. */
public class Color_Picker extends JPanel
                              implements ChangeListener{

    public static JColorChooser tcc;
    public static JLabel banner;

    public Color_Picker() {
        super(new BorderLayout());

        //Need a button to say that the user selected a color

        JButton selectButton = new JButton("Select Color");
        selectButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                SelectButtonClick();
            }
        });

        //Set up color chooser for setting text color
        tcc = new JColorChooser();
        tcc.getSelectionModel().addChangeListener(this);
        tcc.setBorder(BorderFactory.createTitledBorder("Choose Element Color"));

        //Add everything to the panel
        add(tcc, BorderLayout.CENTER);
        add(selectButton, BorderLayout.PAGE_END);
    }

    public void SelectButtonClick(){
      //output r, g, b once the button is clicked
      Color newColor = tcc.getColor();
      System.out.println(Integer.toString(newColor.getRed()));
      System.out.println(Integer.toString(newColor.getGreen()));
      System.out.println(Integer.toString(newColor.getBlue()));
      System.exit(0);
    }

    public void stateChanged(ChangeEvent e) {

    }

    private static void createAndShowGUI() {
        //Create and set up the window.
        JFrame frame = new JFrame("Color Chooser");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        //Create and set up the content pane.
        JComponent newContentPane = new Color_Picker();
        newContentPane.setOpaque(true); //content panes must be opaque
        frame.setContentPane(newContentPane);

        //Display the window.
        frame.pack();
        frame.setVisible(true);
    }

    public static void main(String[] args) {
        //Schedule a job for the event-dispatching thread:
        //creating and showing this application's GUI.
        javax.swing.SwingUtilities.invokeLater(new Runnable() {
            public void run() {
                createAndShowGUI();
            }
        });
    }
}
