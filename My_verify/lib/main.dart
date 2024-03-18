import 'package:flutter/material.dart';
import 'package:my_verify/pages/check_image.dart';
import 'package:my_verify/pages/check_text.dart';
import 'package:my_verify/pages/check_link.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Demo Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  int index = 0;
  final screen = [
    CheckImage(), // Added CheckImage here
    Center(child: Text("Check Video", style: TextStyle(fontSize: 72))),
    CheckLink(),
    CheckTextPage()
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: screen[index],
      bottomNavigationBar: NavigationBarTheme(
        data: NavigationBarThemeData(
          indicatorColor: Colors.blue.shade100,
          labelTextStyle: MaterialStateProperty.all(
              TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
        ),
        child: NavigationBar(
          height: 70,
          backgroundColor: const Color(0xFFf1f5fb),
          selectedIndex: index,
          onDestinationSelected: (index) => setState(() => this.index = index),
          destinations: const [
            NavigationDestination(
              icon: Icon(Icons.camera_alt_outlined),
              selectedIcon: Icon(Icons.camera_alt),
              label: "Check Image",
            ),
            NavigationDestination(
              icon: Icon(Icons.video_call_outlined),
              selectedIcon: Icon(Icons.video_call),
              label: "Check Video",
            ),
            NavigationDestination(icon: Icon(Icons.link), label: "Check Link"),
            NavigationDestination(
              icon: Icon(Icons.text_fields_outlined),
              selectedIcon: Icon(Icons.text_fields),
              label: "Check Text",
            ),
          ],
        ),
      ),
    );
  }
}
