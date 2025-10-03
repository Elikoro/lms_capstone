from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    def __str__(self): return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self): return self.name

class Course(models.Model):
    STATUS = (('draft','Draft'),('published','Published'))
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.SET_NULL,related_name='courses')
    tags = models.ManyToManyField(Tag,blank=True,related_name='courses')
    price = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    instructor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='courses')
    status = models.CharField(max_length=20,choices=STATUS,default='draft')
    published_at = models.DateTimeField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def save(self,*a,**k):
        if not self.slug: self.slug = slugify(self.title)
        if self.status=='published' and self.published_at is None: self.published_at = timezone.now()
        super().save(*a,**k)
    def __str__(self): return self.title

class Module(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=1)
    class Meta: ordering = ['order']
    def __str__(self): return f"{self.course.title} - {self.title}"

class Lesson(models.Model):
    CONTENT_TYPES = (('video','Video'),('pdf','PDF'),('text','Text'))
    module = models.ForeignKey(Module,on_delete=models.CASCADE,related_name='lessons')
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=10,choices=CONTENT_TYPES,default='text')
    content = models.TextField(blank=True)
    file = models.FileField(upload_to='lessons/',blank=True,null=True)
    url = models.URLField(blank=True,null=True)
    duration = models.DurationField(null=True,blank=True)
    order = models.PositiveIntegerField(default=1)
    class Meta: ordering = ['order']
    def __str__(self): return f"{self.module.title} - {self.title}"

class LessonProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='lesson_progress')
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,related_name='progresses')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True,blank=True)
    class Meta:
        unique_together = ('student','lesson')
    def __str__(self): return f"{self.student.username} - {self.lesson.title}"
