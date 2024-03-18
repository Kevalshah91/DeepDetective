import 'package:flutter/material.dart';

class CheckLink extends StatefulWidget {
  @override
  _CheckLinkState createState() => _CheckLinkState();
}

class _CheckLinkState extends State<CheckLink> {
  TextEditingController _inputController = TextEditingController();
  TextEditingController _outputController = TextEditingController();

  void _handleSubmit() {
    // Perform any processing here before updating the output text field
    String inputText = _inputController.text;
    // For demonstration, just echoing back the input text
    _outputController.text = inputText;

    // Here you can pass the output to your ML model for further processing
    // For example:
    // myMLModel.predict(inputText);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Check Link'),
      ),
      body: Padding(
        padding: EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            TextField(
              controller: _inputController,
              decoration: InputDecoration(
                labelText: 'Input Text',
              ),
            ),
            SizedBox(height: 16.0),
            ElevatedButton(
              onPressed: _handleSubmit,
              child: Text('Submit'),
            ),
            SizedBox(height: 16.0),
            TextField(
              controller: _outputController,
              decoration: InputDecoration(
                labelText: 'Output Text',
              ),
              readOnly: true,
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _inputController.dispose();
    _outputController.dispose();
    super.dispose();
  }
}
