<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Population Genetics Web Tool - Project Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        h1, h2, h3 { color: #333; }
        p, ul, ol { margin-bottom: 1.2rem; }
        code { background-color: #f4f4f4; padding: 2px 4px; }
    </style>
</head>
<body>
    <h1>Population Genetics Web Tool</h1>
    <p>This GitHub repository hosts the source code for a web-based software tool developed as part of the MSC Bioinformatics Software Development Group Project 2024. The project's primary objective is to create a functional prototype for handling molecular biology data, with a specific focus on human population genetics.</p>
    
    <h2>Project Overview</h2>
    <p>The application facilitates the analysis of genetic data collected from a Siberian population, alongside data from the 1000 Genomes Project, to understand population structure and genetic admixture. It allows users to perform clustering analysis, admixture analysis, retrieve allele and genotype frequencies for SNPs, and compare genetic differentiation across populations.</p>

    <h2>System Architecture</h2>
    <h3>Backend</h3>
    <ul>
        <li><strong>Flask Application:</strong> Serves as the backbone of the application, handling routing, session management, and communication between the frontend and the database.</li>
        <li><strong>SQLite Database:</strong> Stores genetic data, population information, and SNP annotations. SQLite was selected for its simplicity and adequacy for handling the data scale required by this project.</li>
        <li><strong>Data Analysis and Visualization:</strong> Utilizes NumPy, Pandas for data manipulation and analysis, and Matplotlib, Seaborn, and Plotly for generating plots and interactive visualizations.</li>
        <li><strong>Session Management:</strong> Flask-Session handles user sessions, allowing for data persistence across different views and analyses.</li>
    </ul>

    <h3>Frontend</h3>
    <ul>
        <li><strong>HTML/CSS:</strong> Utilizes HTML templates extended from a base layout with a focus on 'Bebas Neue' font and a cohesive color scheme for a consistent look and feel.</li>
        <li><strong>JavaScript:</strong> Facilitates interactive elements and dynamic content loading, including triggering analyses and rendering Plotly charts.</li>
    </ul>

    <h2>Data Management and Analysis</h2>
    <p>Integrates genetic data with annotations for SNP clinical relevance and population information, providing functionalities for clustering and admixture analysis, SNP information retrieval, and visualization of pairwise population genetic differentiation.</p>

    <h2>Security and Accessibility</h2>
    <p>Emphasizes input validation to prevent SQL injection and XSS attacks, adhering to web standards for compatibility across various devices and screen sizes.</p>

    <h2>User Guide and Tutorials</h2>
    <p>Provides step-by-step guides on performing analyses, interpreting results, and navigating the application through a dedicated <code>tutorials.html</code> page.</p>

    <h2>Deployment and Future Work</h2>
    <p>Outlines the prototype's status, designed for demonstration purposes, with plans for future development focusing on optimizing performance, enhancing security features, and expanding the dataset.</p>

    <h2>Project Timeline</h2>
    <p>Project Start Date: Monday, 22nd January<br>Project End Date: Friday, 1st March</p>

    <h2>Technologies Used</h2>
    <p>SQL, Flask, SQLite, NumPy, Pandas, Matplotlib, Seaborn, Plotly, HTML, CSS, JavaScript</p>

    <h2>How to Use</h2>
    <ol>
        <li>Clone the repository to your local machine.</li>
        <li>Install the required dependencies listed in the project documentation.</li>
        <li>Run the web application using your preferred development environment.</li>
        <li>Follow the user interface to perform analyses and retrieve genetic information.</li>
    </ol>

    <h2>Contributors</h2>
    <ul>
        <li>Your Name</li>
        <li>Your Teammate's Names</li>
    </ul>

    <h2>License</h2>
    <p>This project is open-source and available under the MIT License.</p>

    <p>For questions or issues, please open an issue in this repository.</p>
</body>
</html>
