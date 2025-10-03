package com.ai.azure.active.directory.gui;

import java.awt.BorderLayout;
import java.sql.SQLException;
import java.util.Vector;

import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;

import com.ai.azure.active.directory.repository.AzureADRepository;

public class UnifiedGUI extends JFrame {

	private static final long serialVersionUID = 1L;

	private JTable userTable;
	private DefaultTableModel model;
	private AzureADRepository repo;

	public UnifiedGUI() {
		setTitle("AI + Azure Active Directory Users");
		setSize(900, 600);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setLocationRelativeTo(null);

		try {
			repo = new AzureADRepository();
			Vector<String> columns = new Vector<>();
			columns.add("ID");
			columns.add("Display Name");
			columns.add("Email");
			columns.add("Job Title");
			columns.add("Risk");

			Vector<Vector<Object>> data = repo.getUsers();
			model = new DefaultTableModel(data, columns);
			userTable = new JTable(model);

			JScrollPane scrollPane = new JScrollPane(userTable);
			add(scrollPane, BorderLayout.CENTER);

		} catch (SQLException e) {
			JOptionPane.showMessageDialog(this, "Database connection failed:\n" + e.getMessage(), "Error",
					JOptionPane.ERROR_MESSAGE);
			e.printStackTrace();
		}

		setVisible(true);
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(UnifiedGUI::new);
	}
}
