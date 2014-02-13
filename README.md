About
=====

Grass is a small script for making the writing of CSS simpler by adding basic variables, and removing the requirement of semi-colons. 

Usage
=====
    
    python grass.py <file.grass>


Examples
========

This is an example that includes all the functionality of Grass.
    
    import test2.gss

    var width = 0
    var red = #FF0000
    .someDiv {

        width: $width
        color: $red
        float: left

    }

