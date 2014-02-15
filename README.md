About
=====

Grass is an extension to CSS that allows for things such as variables, nesting, and importing of other style sheets making the web design process much more enjoyable.

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

        width: $width;
        color: $red;
        float: left;
        li {
    
            color: #000; // Some nested div
        }
    }

