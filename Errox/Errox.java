package Errox;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.SwingUtilities;
import java.awt.BorderLayout;
public class Errox
{
    public static void main(String[] args)
    {
        for(int i=0; i<100; i++)
        {
            SwingUtilities.invokeLater(() -> {
                JDialog dialog = new JDialog();
                dialog.setTitle("ERROR");
                JLabel messageLabel = new JLabel("ERROX!");
                dialog.add(messageLabel, BorderLayout.CENTER);
                dialog.setSize(150, 100);
                dialog.setLocationRelativeTo(null);
                dialog.setDefaultCloseOperation((JDialog.DISPOSE_ON_CLOSE));
                dialog.setModalityType(JDialog.ModalityType.MODELESS);
                dialog.setVisible(true);
            });
        }
    }
}
