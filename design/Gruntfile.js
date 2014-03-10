module.exports = function (grunt) {
    "use strict";
 
    grunt.registerTask('watch', [ 'watch' ]);
 
    grunt.initConfig({
        concat: {
            js: {
                options: {
                    separator: ';'
                },
                src: [
                    'src/js/*.js'
                ],
                dest: 'public/scripts/js/ark.min.js'
            }
        },
        uglify: {
            options: {
                mangle: false
            },
            js: {
                files: {
                    'public/scripts/js/ark.min.js': ['public/scripts/js/ark.min.js']
                }
            }
        },
        less: {
            style: {
                files: {
                    "public/scripts/css/ark.css": "src/less/ark.less",
                    "public/scripts/css/theme.css": "src/less/theme.less",
                    "public/scripts/css/prettify.css": "src/less/prettify.less",
                    "public/scripts/css/examples.css": "src/less/examples.less"
                }
            }
        },
        assemble: {
            options:{
                layoutdir: 'src/html/layouts'
            },
            inner:{
                options: {
                    layout: 'default.hbs',
                    flatten: true
                },
                src: ['src/html/pages/default/*.hbs'],
                dest: 'public/'
            },
            login:{
                options: {
                    layout: "login.hbs",
                    flatten: true
                },
                src: ['src/html/pages/login/*.hbs'],
                dest: 'public/'
            }
        },
        clean: {
            all: ['public/*.html']
        },
        watch: {
            js: {
                files: ['src/js/*.js'],
                tasks: ['concat:js', 'uglify:js'],
                options: {
                    livereload: true
                }
            },
            css: {
                files: ['src/less/*.less','src/less/**/*.less'],
                tasks: ['less:style'],
                options: {
                    livereload: true
                }
            },
            assemble: {
                files: ['src/html/**/*.hbs'],
                tasks: ['assemble:inner', 'assemble:login'],
                options: {
                    livereload: true
                }
            }
        }
    });
 
    grunt.loadNpmTasks('assemble');
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-less');
    grunt.loadNpmTasks('grunt-contrib-watch');
    
    grunt.registerTask('default', ['clean', 'concat:js', 'uglify:js', 'less:style', 'assemble:inner', 'assemble:login', 'watch']);
 
};