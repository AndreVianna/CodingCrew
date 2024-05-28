# FacePuppy - Project Summary Report

## Project Brief Summary

FacePuppy is a web application designed for puppy owners to create and manage profiles for their pets. The platform allows users to register, create and manage puppy profiles, upload photos, write blog posts, search for other users' puppies, and view their blog posts. Administrators have access to an admin dashboard for managing user content. The application is mobile-responsive and aims to build a community of puppy lovers.

## Project Goals and Objectives

The primary goal of FacePuppy is to provide a user-friendly platform for puppy owners to manage and share their puppies' profiles, photos, and blog posts. The objectives include:

- Enabling users to create and manage detailed puppy profiles.
- Allowing users to upload and manage photos in a gallery.
- Providing a platform for users to write and share blog posts about their puppies.
- Implementing search functionality to find and view other users' puppies.
- Developing an admin dashboard for content management.
- Ensuring the application is mobile-responsive.

## Project Scope

The project scope includes the development of a web application using Flutter Web for the frontend and Node.js for the backend. The application will feature user registration and login, puppy profile management, photo gallery, blog posts, search functionality, and an admin dashboard. The project will also include thorough testing, documentation, and refinement based on feedback.

## Major Features

- **User Registration and Login**: Secure user registration and login using OAuth2.
- **Puppy Profile Management**: Users can create and maintain detailed profiles for their puppies.
- **Photo Gallery**: Users can upload and manage photos in a gallery with a grid layout and lightbox feature.
- **Blog Posts**: Users can write and share blog posts with embedded images and a rich text editor.
- **Search Functionality**: Users can search for and view other users' puppy profiles.
- **Follow Functionality**: Users can follow other puppies.
- **Admin Dashboard**: Administrators can manage users' content and profiles.
- **Mobile-Responsive Design**: The application is designed to be mobile-responsive.

## Major Components

- **Frontend**: Developed using Flutter Web.
- **Backend**: Developed using Node.js.
- **Authentication**: Implemented using OAuth2.
- **Data Storage**: JSON files organized under a 'data' folder.

## Professional Resources

- **Frontend Developer (2)**: Skilled in Flutter Web, responsible for developing the user interface and ensuring mobile responsiveness.
- **Backend Developer (2)**: Skilled in Node.js, responsible for developing the server-side logic and data storage.
- **UI/UX Designer (1)**: Responsible for designing the user interface and ensuring an intuitive user experience.
- **QA Engineer (1)**: Responsible for testing the application to ensure all features work as expected.
- **Project Manager (1)**: Responsible for overseeing the project, coordinating between team members, and ensuring timely delivery.

## Assumptions, Constraints, and Risks

### Assumptions

- **Internet Access**: Users have access to the internet and a web browser.
- **User Familiarity**: Users are familiar with basic web application navigation.
- **Reliable Hosting**: The application will be hosted on a reliable server.
- **Accurate Information**: Users will provide accurate and truthful information about their puppies.

### Constraints

- **Technology Stack**: The project must be developed using Flutter Web for the frontend and Node.js for the backend.
- **Design Adherence**: The project must adhere to the specified design preferences and layout requirements.
- **Time and Budget**: The project must be completed within the allocated time and budget.
- **Regulatory Compliance**: The project must comply with data protection and privacy regulations.

### Risks

- **Security Vulnerabilities**: Potential security vulnerabilities in user registration and login processes.
- **Performance Issues**: Performance issues due to high traffic or large amounts of data.
- **Development Delays**: Delays in development due to unforeseen technical challenges.
- **User Adoption**: User adoption and engagement may be lower than expected.

## Target Audience

The target audience includes puppy owners who want to create and share profiles for their puppies, as well as other users who are interested in viewing and following puppies. The application is designed for users of all ages who have an interest in puppies.

## Backend Requirements

### Security

#### Authentication

- Secure user registration and login using OAuth2.
- Users must provide their name, email, and password during registration.
- Passwords should be stored hashed in the user file located in their respective folder.

#### Authorization

- Users can have up to 2 roles: User or Administrator.
- Only users with the role of Administrator can access the admin dashboard.

### Data, External Connections (API, Services, etc)

#### Data Storage

- All data should be stored in JSON files organized under a folder named 'data' as part of the backend.
- Each user should have a dedicated folder under 'users', named by their user id.
- Each puppy should have a dedicated folder under 'puppies', named by their puppy id.
- Under each individual puppy's folder, there should be two subfolders: 'gallery' for photos and 'blog' for blog posts.
- Directly under the 'data' folder, there should be a file named 'user_email.json' containing a mapping from user email to user id.
- Directly under the 'data' folder, there should be a file named 'puppy_owner.json' containing a mapping from puppy id to user id.

#### External Connections

- The application will use OAuth2 for secure user authentication.
- The application may integrate with external email services for sending contact form queries.

## Frontend Requirements

### UI Framework

The project will use Flutter Web for the frontend development.

### Design Preferences

- The main palette colors should be (but not restricted to) light blue and light green.
- The navigation must be intuitive and easy-to-use across all pages.
- The gallery must have a grid layout for photo display with lightbox feature for enlarged view.
- The blog page must have a traditional blog layout.
- The search bar must be prominently displayed for easy access.
- There must be a colorful landing page for guests rich with puppy stock photos, sections, and call-to-action buttons.
- The logged in users landing page must show a card for each of the user's puppy, the last few images added to the gallery across all of his puppies, and the last few blog posts added across all of his puppies, and the latest updates of the puppies that user follows.
- There must be a colorful about page also rich with puppy stock photos.
- There must be a traditional contact page with a form to capture the user queries and send by email.
- Clean and intuitive admin dashboard layout with data and visualization.

### Views/Pages and Navigation

- **Landing Page**: A colorful landing page for guests with puppy stock photos and call-to-action buttons.
- **User Registration and Login Pages**: Pages for user registration and login.
- **User Dashboard**: Showing cards for each puppy, recent gallery images, blog posts, and updates from followed puppies.
- **Puppy Profile Page**: Detailed information and photo gallery for each puppy.
- **Blog Page**: Traditional blog layout with a rich text editor.
- **Search Page**: Search bar and results display.
- **About Page**: Rich with puppy stock photos.
- **Contact Page**: Form to capture user queries and send by email.
- **Admin Dashboard**: For managing users' content and profiles.

## Additional Information

- The project must be documented with a README file containing the project name, description, scope, technical details, and instructions for running the project.
- The project must be tested thoroughly to ensure all features work as expected.
- The project must be reviewed and refined based on feedback from stakeholders and users.
