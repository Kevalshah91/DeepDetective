import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

class CheckImage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Select an Image',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: ImagePickerDemo(),
    );
  }
}

class ImagePickerDemo extends StatefulWidget {
  @override
  _ImagePickerDemoState createState() => _ImagePickerDemoState();
}

class _ImagePickerDemoState extends State<ImagePickerDemo> {
  Uint8List? _imageBytes;
  final picker = ImagePicker();

  Future getImage(ImageSource source) async {
    final pickedFile = await picker.pickImage(source: source);

    setState(() {
      if (pickedFile != null) {
        pickedFile.readAsBytes().then((bytes) {
          setState(() {
            _imageBytes = Uint8List.fromList(bytes);
          });
        });
      } else {
        print('No image selected.');
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Pick an Image'),
      ),
      body: Center(
        child: _imageBytes == null
            ? Text('No image selected.')
            : Image.memory(_imageBytes!),
      ),
      floatingActionButton: Column(
        mainAxisAlignment: MainAxisAlignment.end,
        children: <Widget>[
          FloatingActionButton(
            onPressed: () {
              getImage(ImageSource.camera);
            },
            tooltip: 'Take Picture',
            child: Icon(Icons.camera_alt),
          ),
          SizedBox(height: 16),
          FloatingActionButton(
            onPressed: () {
              getImage(ImageSource.gallery);
            },
            tooltip: 'Pick Image',
            child: Icon(Icons.photo_library),
          ),
        ],
      ),
    );
  }
}
