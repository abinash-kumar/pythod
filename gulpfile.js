module.exports = {
   plugins: [
       require('precss'),
       require('autoprefixer')
   ]
}

var postcss = require('gulp-postcss');
var gulp = require('gulp');
var sourcemaps = require('gulp-sourcemaps');
var sass = require('gulp-sass');


gulp.task('css', function () {
   return gulp.src(['static_content/postcss/style_mobile.scss', 'static_content/postcss/style.scss'])
       .pipe( sass())
       .pipe( sourcemaps.init() )
       .pipe( postcss([ require('precss'), require('autoprefixer') ]) )
       .pipe( sourcemaps.write('.') )
       .pipe( gulp.dest('static_content/css/') );
});

gulp.task('watch', function(){
       gulp.watch(['static_content/postcss/style.scss', 'static_content/postcss/style_mobile.scss'], ['css'])
});
