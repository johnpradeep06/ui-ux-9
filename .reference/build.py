from pathlib import Path
import json, html

ROOT = Path(__file__).resolve().parent.parent
refs = json.loads((ROOT / '.reference/design-context.json').read_text(encoding='utf-8'))
screens = [('login', 'Sign in', 'Frame'), ('dashboard', 'Dashboard', 'Frame 1'), ('academics', 'Academics', 'Frame 2'), ('notifications', 'Notifications', 'Frame 3'), ('submission', 'Submission', 'Frame 4')]

def icon(i, key, w=20, h=None, extra=''):
    h = h or w
    return f'<img src="assets/{refs[i]["assets"]["img"+key]}" width="{w}" height="{h}" alt="" {extra}>'

def status(i):
    return f'<header class="status-bar" aria-label="Device status"><span>9:41</span><div class="device-status">{icon(i,"IosSignal",17)}{icon(i,"IosWifiSignal",17)}{icon(i,"IosBatteryFull",25,17)}</div></header>'

def home(): return '<div class="home-indicator" aria-hidden="true"></div>'

def nav(i, active):
    items = [('dashboard','Home','House'),('academics','Academics','BookOpen'),('notifications','Updates','Bell'),('profile','Profile','UserRound')]
    out = '<footer class="bottom-nav"><nav class="destinations" aria-label="Main navigation">'
    for route,label,img in items:
        attrs = 'aria-current="page"' if route == active else ''
        cls = 'nav-item active' if route == active else 'nav-item'
        inner=f'<span class="nav-icon">{icon(i,img)}</span><span>{label}</span>'
        if route=='profile': out += f'<button class="{cls}" type="button" data-dialog="profile-dialog">{inner}</button>'
        else: out += f'<a class="{cls}" href="{route}.html" {attrs}>{inner}</a>'
    return out + '</nav>' + home() + '</footer>'

def button(label, target, secondary=False, spacer=True):
    return f'<a class="{"secondary" if secondary else "primary"}" href="{target}.html">'+('<span class="action-spacer" aria-hidden="true"></span>' if spacer else '')+label+'</a>'

def dialogs():
    return '''<dialog id="info-dialog" aria-labelledby="info-title"><button class="dialog-close" data-close aria-label="Close dialog">×</button><h2 id="info-title"></h2><p id="info-message"></p><button class="primary" data-close>Got it</button></dialog>
<dialog id="profile-dialog" aria-labelledby="profile-title"><button class="dialog-close" data-close aria-label="Close profile">×</button><h2 id="profile-title">John</h2><p>john.doe@university.edu</p><a class="primary" href="login.html">Sign out</a><button class="secondary" data-close>Close</button></dialog>
<dialog id="assignment-dialog" aria-labelledby="assignment-title"><button class="dialog-close" data-close aria-label="Close assignment">×</button><h2 id="assignment-title">Problem Set 04</h2><p>Data Structures<br>Due Fri, Oct 16 · 11:59 PM</p><form id="assignment-form"><label for="assignment-file">Choose your assignment</label><input id="assignment-file" type="file" required><p class="tiny">Prototype preview: the selected file stays on your device.</p><button class="primary" type="submit">Submit assignment</button><button class="secondary" type="button" data-close>Cancel</button></form></dialog>
<dialog id="preferences-dialog" aria-labelledby="preferences-title"><button class="dialog-close" data-close aria-label="Close preferences">×</button><h2 id="preferences-title">Notification preferences</h2><form id="preferences-form"><label><input type="checkbox" name="assignments" checked> Assignments</label><label><input type="checkbox" name="attendance" checked> Attendance</label><label><input type="checkbox" name="registration" checked> Course registration</label><button class="primary" type="submit">Save preferences</button></form></dialog>'''

def write_screen(i, body, active=None):
    route,title,_=screens[i]
    footer=nav(i,active) if active else home()
    doc=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f5f6fa"><title>{title} · ASS9</title><link rel="stylesheet" href="styles.css"><script defer src="app.js"></script></head>
<body><div class="phone {'bordered' if i in (1,2,3) else ''} {route}" data-figma-node="{refs[i]['id']}">{status(i)}{body}{footer}</div>{dialogs()}</body></html>'''
    (ROOT/f'{route}.html').write_text(doc,encoding='utf-8')

write_screen(0, f'''<main class="signin-content"><div class="welcome-and-form"><section class="welcome"><div class="portal-badge">STUDENT PORTAL</div><h1>Welcome back</h1><p>Sign in to check your dashboard and stay on top of your semester.</p></section>
<form class="signin-form" id="signin-form" action="dashboard.html">
<div class="field"><label for="student-id">Student ID or Email</label><div class="input-shell"><input id="student-id" name="student" type="text" value="john.doe@university.edu" autocomplete="username" required></div></div>
<div class="field"><label for="password">Password</label><div class="input-shell"><input id="password" name="password" type="password" value="password" autocomplete="current-password" required><button class="show-password" type="button" aria-label="Show password" aria-pressed="false">{icon(0,'ShowPassword')}</button></div></div>
<div class="signin-options"><label class="remember"><input type="checkbox" name="remember" checked><span class="checkbox">{icon(0,'Checked',14)}</span><span>Remember me</span></label><button class="forgot" type="button" data-info="recovery">Forgot password?</button></div>
<button class="primary" type="submit"><span class="action-spacer" aria-hidden="true"></span>Sign in</button></form></div>
<div class="account-support"><p>Don't have an account?</p><button type="button" data-info="admin">Contact Admin</button></div></main>''')

write_screen(1,f'''<main class="content"><header class="page-header"><h1>Hey there, John</h1></header>
<section class="semester"><p class="eyebrow">FALL 2026 · WEEK 7</p><h2>A strong semester so far.</h2><p>Keep your momentum. You've got this.</p><p class="gpa">3.8 GPA</p></section>
<section class="metrics" aria-label="Academic overview"><a href="academics.html" class="card metric"><div class="metric-heading"><span>Attendance</span>{icon(1,'CalendarCheck',16)}</div><div class="metric-value"><strong>92%</strong><span>23 / 25</span></div></a><a class="card metric" href="academics.html#assignments"><div class="metric-heading"><span>Assignments</span>{icon(1,'ClipboardList',16)}</div><div class="metric-value"><strong>3</strong><span>to do</span></div></a></section>
<section class="section"><h2>Today's classes</h2><div class="card class-list"><a class="scheduled-class" href="academics.html"><div class="class-time">10:00<span>11:30</span></div><span class="course-marker"></span><div class="class-info"><h3>Data Structures</h3><p>CS204 · Room B-204</p></div></a><div class="divider"></div><div class="scheduled-class"><div class="class-time">13:00<span>14:00</span></div><span class="course-marker pale"></span><div class="class-info"><h3>Linear Algebra</h3><p>MA202 · Room A-112</p></div></div></div></section>
<section class="section todo"><h2>On your to-do list</h2><a href="academics.html#assignments" class="card todo-card"><span class="icon-box">{icon(1,'FileText')}</span><div class="todo-info"><h3>Problem Set 04</h3><p>Due Fri, Oct 16 · 11:59 PM</p></div></a><a href="academics.html#assignments" class="card todo-card"><span class="icon-box">{icon(1,'FileText')}</span><div class="todo-info"><h3>Matrix Transformations</h3><p>Due Mon, Oct 19 · 11:59 PM</p></div></a></section></main>''','dashboard')

days=''.join(f'<div class="attendance-day"><span class="attendance-status {"absent" if d=="05" else ""}" aria-label="{"Absent" if d=="05" else "Present"}">{icon(2,"X" if d=="05" else "Check",15)}</span><span>{d}</span></div>' for d in ['02','05','07','09','12'])
write_screen(2,f'''<main class="content"><header class="page-header"><h1>Academics</h1><button class="icon-button" type="button" data-info="calendar" aria-label="View academic calendar">{icon(2,'CalendarDays')}</button></header>
<button class="card course-select" type="button" data-info="course"><span class="icon-box">{icon(2,'CodeXml')}</span><strong class="grow">Data Structures</strong>{icon(2,'ChevronDown',18)}</button>
<section class="section"><h2>Attendance</h2><div class="card attendance-card"><div class="attendance-performance"><div class="attendance-ring" aria-label="92 percent attendance">{icon(2,'ProgressTrack',82)}{icon(2,'AttendanceProgress',82)}<strong>92%</strong></div><div class="attendance-context"><h3>You're on track</h3><p class="tiny muted">23 of 25 classes attended</p><span class="badge">Above 75% requirement</span></div></div><div class="divider"></div><h3 class="recent-classes-label">Recent classes</h3><div class="recent-classes">{days}</div></div></section>
<section class="section" id="assignments"><h2>Assignments</h2><article class="card upcoming-assignment"><span class="badge todo-badge">To do</span><h3>Problem Set 04</h3><p class="deadline">{icon(2,'Clock3',14)}<span>Fri, Oct 16 · 11:59 PM · 2 days left</span></p><button class="primary" type="button" data-dialog="assignment-dialog"><span class="action-spacer" aria-hidden="true"></span>View assignment</button></article><article class="card graded-assignment"><span class="icon-box">{icon(2,'FileCheck2',19)}</span><h3 class="grow">Sorting Algorithms Lab</h3><span class="grade">18/20</span></article></section></main>''','academics')

def notice(title,key,description='',cls='',unread=False,category='assignments',mint=False):
    dot=icon(3,'UnreadIndicator',6,extra='class="unread-dot"') if unread else ''
    return f'''<article class="card notification {cls} {'unread' if unread else ''}" data-category="{category}" data-unread="{str(unread).lower()}"><span class="icon-box {'mint' if mint else ''}">{icon(3,key,18)}</span><div class="notification-info"><div class="notification-heading"><h3>{title}</h3>{dot}</div>{'<p>'+html.escape(description)+'</p>' if description else ''}</div></article>'''

write_screen(3,f'''<main class="content"><header class="page-header"><h1>Notifications</h1><button class="icon-button" type="button" data-dialog="preferences-dialog" aria-label="Notification preferences">{icon(3,'SlidersHorizontal')}</button></header>
<div class="filters" role="group" aria-label="Filter notifications"><button class="filter active" type="button" data-filter="all" aria-pressed="true">All updates</button><button class="filter" type="button" data-filter="unread" aria-pressed="false">Unread  <span id="unread-count">3</span></button><button class="filter" type="button" data-filter="deadlines" aria-pressed="false">Deadlines</button></div>
<section class="section notification-group"><div class="date-heading"><h2 class="small">Today</h2><button type="button" id="mark-read">Mark all as read</button></div>{notice('New assignment posted','ClipboardList',cls='compact',unread=True)}{notice('A new room for CS204','MapPin',cls='room',unread=True,category='course')}</section>
<section class="section notification-group"><div class="date-heading"><h2 class="small">Yesterday</h2><time datetime="2026-10-13">October 13</time></div>{notice('Your lab grade is in','BadgeCheck',"CS204 · You earned 18/20 on Sorting Algorithms Lab. See Dr. Park's feedback.",unread=True,mint=True)}{notice('Attendance updated','CalendarCheck','CS204 · 23 of 25 classes attended. Your attendance is holding strong at 92%.',category='attendance')}{notice('Plan your next semester','GraduationCap','Spring course registration opens Oct 26. Meet your advisor to get ready.',cls='registration',category='registration')}</section><p class="empty-notifications" hidden>No notifications to show.</p></main>''','notifications')

write_screen(4,f'''<main class="content submission-content"><header class="page-header"><h1>Submission</h1></header><div class="confirmation-area"><section class="card confirmation-card"><div class="success-emblem">{icon(4,'SuccessCheck',46)}</div><div class="confirmation-message"><h2>Successfully submitted</h2><p>Your assignment has been submitted. You can return to Academics to review it.</p></div><div class="submitted-assignment"><p>DATA STRUCTURES</p><h3>Problem Set 04</h3><div class="submission-status">{icon(4,'StatusCheck',16)}<span>Submitted</span></div></div><div class="next-actions">{button('Back to academics','academics')}{button('Go to dashboard','dashboard',True)}</div></section></div></main>''','academics')

frames=''.join(f'<figure class="frame-preview"><figcaption><span>{frame} · {title}</span><a href="{route}.html">Open screen ↗</a></figcaption><iframe title="{title}" src="{route}.html"></iframe></figure>' for route,title,frame in screens)
(ROOT/'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>ASS9 · All five screens</title><link rel="stylesheet" href="styles.css"></head><body class="gallery"><header class="gallery-header"><div><h1>ASS9</h1><p>Five original frames · 402 × 992</p></div><a href="login.html">Start prototype ↗</a></header><main class="frames">{frames}</main></body></html>''',encoding='utf-8')
print('Created six HTML pages.')
