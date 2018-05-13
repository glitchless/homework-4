Testing ok.ru for Technopark's QA course

Usage:

1. Run grid.sh
2. Run node.sh
3. Set `BROWSER` env variable with something of [`FIREFOX`, `CHROME`], 
4. Set `PASSWORD` and `LOGIN` env variables with working ok's login-password pair
5. Run basic_grid to ensure everything works fine
6. Run run_tests.py

WARNING: geckodriver located in this repo is for Mac OS X only!
Replace it locally if you need to set up a selenium environment for another system.