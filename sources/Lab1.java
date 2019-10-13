import java.awt.Color;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JFrame;


class Button extends JButton implements ActionListener {

	private static final long serialVersionUID = 1L;
	public  static enum   States {STATE1, STATE2};
	
	private Color  color1, color2;
	private String text1,  text2;
	private States state;

	public Button(Color color1, Color color2, String text1, String text2) {
		this.color1 = color1;
		this.color2 = color2;
		this.text1  = text1;
		this.text2  = text2;
		this.state  = States.STATE1;
		

		// https://stackoverflow.com/questions/1065691/how-to-set-the-background-color-of-a-jbutton-on-the-mac-os
		this.setText(text1);
		this.setOpaque(true);
		this.setBorderPainted(false);
		this.setBackground(color1);
		this.addActionListener(this);
	}

	public void toggleState() {
		if (this.state == States.STATE1) {
			this.state = States.STATE2;
			this.setText(text2);
			this.setBackground(color2);
		} else {
			this.state = States.STATE1;
			this.setText(text1);
			this.setBackground(color1);
		}
	}

	public States getState() {
		return this.state;
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		toggleState();
	}
	
}


class Window extends JFrame {

	private static final long serialVersionUID = 1L;
	private static final int  WIDTH  = 480;
	private static final int  HEIGHT = 360;
	
	private List<Button> buttons = new ArrayList<Button>();

	public Window(String title, String[] buttonText) {
		super(title);

		this.getContentPane().setBackground(Color.DARK_GRAY);

		this.setSize(WIDTH, HEIGHT);
		this.setResizable(false);
		this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		this.setLayout(new GridLayout(buttonText.length / 2, 1));
		
		for (int i = 0; i < buttonText.length; i += 2) {
			Button button = new Button(Color.GREEN, Color.RED, buttonText[i], buttonText[i+1]);
			this.add(button);
			buttons.add(button);
		}
		
		this.setVisible(true);
	}

	
//	@Override
//	public void actionPerformed(ActionEvent e) {
//
//		Button button = (Button) e.getSource();
//		if (button.getState() == Button.States.STATE1) {
//			this.label.setText("NOOO!!! WHAT DID YOU DO!?");
//		} else {
//			this.label.setText("Nothing to show...");
//		}
//		button.toggleState();
//	}
}


public class Lab1 {
	
	public static void main(String[] args) {
		
		if (args.length % 2 != 0) {
			System.err.println("Must pass an even number of arguments!");
			System.exit(-1);
		}
		for (String a : args) {
			System.out.println(a);
		}
		
		if (args.length > 0) {
			new Window("Lab 1 - program by Ted Klein Bergman", args);
		} else {
                        System.out.println("Creating defualt buttons.");
			String[] arguments = {"Click!", "Don't click!", "Go!", "Stop"};
			new Window("Lab 1 - program by Ted Klein Bergman", arguments);	
		}
	}
}







