<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Company Financial Data</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table, th, td {
            border: 1px solid black;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>

<h2>Company Financial Data</h2>

<table>
    <tr>
        <th>Symbol</th>
        <th>Company Name</th>
        <th>Earnings Yield</th>
        <th>Return on Equity</th>
    </tr>

    <?php
    // 1. Connect to the SQLite database
    try {
        $conn = new PDO("sqlite:C:/Users/tman0/OneDrive/Documents/Code\Magic Formula Project/results.db");
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

        // 2. Prepare and execute a query
        $stmt = $conn->query("SELECT * FROM companies");

        // 3. Fetch and display the results in an HTML table
        while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
            echo "<tr>";
            echo "<td>" . htmlspecialchars($row['symbol']) . "</td>";
            echo "<td>" . htmlspecialchars($row['company_name']) . "</td>";
            echo "<td>" . htmlspecialchars($row['earnings_yield']) . "</td>";
            echo "<td>" . htmlspecialchars($row['return_on_equity']) . "</td>";
            echo "</tr>";
        }

    } catch (PDOException $e) {
        echo "Error: " . $e->getMessage();
    }

    // Close the connection
    $conn = null;
    ?>
</table>

</body>
</html>
