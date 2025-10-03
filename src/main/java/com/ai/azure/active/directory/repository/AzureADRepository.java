package com.ai.azure.active.directory.repository;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Vector;

public class AzureADRepository {

	private static final String DB_URL = "jdbc:mysql://localhost:3306/ai_azure_active_directory?useSSL=false&allowPublicKeyRetrieval=true";
	private static final String DB_USER = "root";
	private static final String DB_PASSWORD = "admin";

	private Connection conn;

	public AzureADRepository() throws SQLException {
		conn = DriverManager.getConnection(DB_URL, DB_USER, DB_PASSWORD);
	}

	public Vector<Vector<Object>> getUsers() throws SQLException {
		Vector<Vector<Object>> data = new Vector<>();

		String query = "SELECT id, displayName, mail, jobTitle, risk FROM azure_users";

		try (Statement stmt = conn.createStatement(); ResultSet rs = stmt.executeQuery(query)) {
			while (rs.next()) {
				Vector<Object> row = new Vector<>();
				row.add(rs.getString("id"));
				row.add(rs.getString("displayName"));
				row.add(rs.getString("mail"));
				row.add(rs.getString("jobTitle"));
				row.add(rs.getString("risk"));
				data.add(row);
			}
		} catch (SQLException e) {
			e.printStackTrace();
		}

		return data;
	}

	public void close() throws SQLException {
		if (conn != null && !conn.isClosed()) {
			conn.close();
		}
	}
}
