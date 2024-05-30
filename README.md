# Web Application with AI Integration 🌐🤖

## About This Project

This project integrates HTML, CSS, and JavaScript to create a web application primarily powered by Flask. Unlike utilizing Watson's API, it opts for Google's speech-to-text and text-to-speech services, reducing complexity while maintaining functionality. The API integration enriches the website's capabilities, facilitating seamless interaction. Leveraging template inheritance using the Jinja2 module, it ensures consistent design and functionality across multiple pages. The project also harnesses the NLTK library of Python for natural language processing tasks. Furthermore, it integrates with Google Cloud services for additional functionalities and scalability. Overall, the project embodies an embeddable AI concept, blending various technologies to deliver a sophisticated yet user-friendly web experience.

## How to Use/Run This Project 🛠️

1. **Set Up a Virtual Environment**
    - Ensure you have Python installed.
    - Create a virtual environment:
      ```bash
      python -m venv venv
      ```
    - Activate the virtual environment:
      - On Windows:
        ```bash
        venv\Scripts\activate
        ```
      - On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

2. **Install Required Libraries**
    - Install the necessary libraries from the `requirements.txt` file:
      ```bash
      pip install -r requirements.txt
      ```

3. **Set Up Google Cloud Services**
    - Sign up for Google Cloud services.
    - Enable Speech-to-Text and Text-to-Speech APIs.
    - Obtain API keys and set up authentication as per Google Cloud's documentation.

4. **Run the Application**
    - Start the Flask server:
      ```bash
      flask run
      ```
    - Open your web browser and navigate to `http://127.0.0.1:5000/` to view the application.

## References 📚

- [CognitiveClass.ai's course "Improve Customer Support with AI-powered Voice Services"](https://cognitiveclass.ai/)
- [Google Cloud's Speech-to-Text documentation](https://cloud.google.com/speech-to-text/docs)

## About Me 👨‍💻

**Chitransh Saxena** is a digital sorcerer, wielding code like magic spells. With a B.Tech from Manipal University, Jaipur, he's deeply into AI and cybersecurity. When not coding, he's strategizing on a chessboard ♟️ or crafting sleek interfaces with HTML, CSS, and JavaScript. Python, C, and C++ are his trusted allies. As Cyber Space VP, he safeguards the digital realm with innovation and humor. Chitransh: where tech meets wit! For more info, check the home page. To reach him, email him at chitrashsaxena67@gmail.com.

## Possible Improvements and Suggestions 💡

- **Speech Recognition Accuracy**: Sometimes the AI model fails to recognize spoken words, especially while recording customer addresses. Consider training the model with more diverse datasets.
- **Bug Fixes**: Occasionally, clicking the continue button results in an `AttributeError` in the `clean_text()` function due to the AI model failing to store processed words.
- **Additional Input Methods**: Adding alternate methods of input, such as text, could enhance usability.
- **Enhancing Address Recognition**: To improve address recording, add specific stop words relevant to your location, similar to how pizza size and toppings are handled. This will make the AI model more specific and accurate.

---

Feel free to reach out for any further assistance or queries! ✉️
