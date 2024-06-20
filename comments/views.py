from django.core.paginator import Paginator
from django.core.mail import get_connection, EmailMultiAlternatives
from django.shortcuts import render, redirect, reverse, Http404
from django.contrib import messages
from django.template.loader import render_to_string
from django.conf import settings
from allauth.account.models import EmailAddress
from comments.models import Comment
from comments.forms import AcceptFormSetBase


def comment_check_view(request, page_num=1):
    # Check if the user is authenticated and has the permission to accept comments
    if request.user.is_authenticated and request.user.has_perm('comments.accept_comment'):
        # Query all unchecked comments, ordered by creation time in descending order
        not_checked_comments = Comment.objects.filter(checked=False).order_by('-datetime_created')
        not_checked_comments_count = not_checked_comments.count()

        # Set the number of comments to display per page
        paginator_count = 20
        pages = Paginator(not_checked_comments, paginator_count)

        # Ensure the requested page number is within valid bounds
        if page_num > pages.num_pages:
            page_num = pages.num_pages
        elif page_num < 1:
            page_num = 1

        # Get the current page of comments
        page = pages.page(page_num)

        # Calculate the indices for comments on the current page
        start_index = (page_num - 1) * paginator_count
        end_index = start_index + paginator_count

        # Get the comments to display on the current page
        this_page_comments = not_checked_comments[start_index:end_index]
        if request.method == 'POST':
            # Handle the form submission when the request method is POST
            formset = AcceptFormSetBase(request.POST, queryset=this_page_comments)
            if formset.is_valid():
                # emails = []
                # Save each form in the formset, marking comments as checked
                connection = get_connection()  # uses SMTP server specified in settings.py
                connection.open()
                for form in formset:
                    comment = form.save(commit=False)
                    comment.checked = True
                    comment.save()
                    email_address = EmailAddress.objects.filter(user=comment.author).first()
                    context = {
                        'comment': comment,
                        'site_name': request.get_host(),
                        'site_url': '{0}://{1}'.format(request.scheme, request.get_host()),
                    }
                    # msg_plain = render_to_string('email/comment_checked.txt', context)
                    # msg_html = render_to_string('email/comment_checked.html', context)
                    # message = (
                    #     "نظر شما در {} بررسی شد".format(context['site_name']),
                    #     msg_plain,
                    #     '<halim-paz@halimpazi.com>',
                    #     [str(email_address)],
                    # )
                    # emails.append(message)
                    html_content = render_to_string('account/email/comment_checked.html', context)
                    text_content = render_to_string('account/email/comment_checked.txt', context)
                    msg = EmailMultiAlternatives('نظر شما در پست "{}" بررسی شد'.format(comment.post.title), text_content, settings.DEFAULT_FROM_EMAIL, [str(email_address)],
                                                 connection=connection)
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()
                connection.close()
                messages.success(request, f"تعداد {len(formset)} نظر بررسی شد و نتیجه بررسی با موفقیت ثبت شد")
                # Redirect to a different page after successful submission
                return redirect(reverse('not_accepted_comments_no_arg'))
        else:
            # Create a formset with the comments for rendering when the request method is not POST
            formset = AcceptFormSetBase(queryset=this_page_comments)

            # Combine forms and comments for rendering
            forms_and_comments_zip = zip(formset, this_page_comments)
            forms_and_comments_list = list(forms_and_comments_zip)

        # Prepare the context for rendering the template
        context = {
            'formset': formset,
            'comments': page,
            'zipped': forms_and_comments_list,
            'page': page,
            'not_checked_comments_count': not_checked_comments_count
        }

        # Render the HTML template with the context
        return render(request, 'comments/not_checked_comments.html', context)
    else:
        # Raise a Http404 exception when the user is not authenticated or lacks the required permission
        raise Http404
