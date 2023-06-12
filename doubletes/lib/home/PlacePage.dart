import 'package:flutter/material.dart';
import 'package:flutter_day1/home/components/categories.dart';

import 'components/navBar.dart';
import 'components/subPlaces.dart';
import 'components/HomeScreen.dart';

class MyHomePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBody: true,
      body: SingleChildScrollView(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            SwiperComponent(),
            TabbarComponent(),
            SizedBox(height: 25),
            FoodListComponent(),
          ],
        ),
      ),
      bottomNavigationBar: BottomNavBar(index: 0),
    );
  }
}
